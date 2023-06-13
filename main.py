import itertools
import json
import logging
import os
import math
import tiktoken
from tqdm import tqdm
from excel import Excel
from ai import Ai
from keyword_analysis import KeywordAnalysis
from globals import PATH, PROMPT, TOKEN_LIMIT, CONTENT_RESPONSE_TOKENS, MESSAGE_PRIMER_TOKENS


def main(ai=True, cut=True, test=False):
    # results table
    chat_gpt_estimations = []

    # initialize OpenAI
    open_ai = Ai()

    src = PATH + "src"
    res = PATH + "res"
    table_path = res

    # initialize Excel input table
    print("Loading source excel table (this may take a while)...", end="")
    excel = Excel(table_path, chat_gpt_estimations)
    print(" Done")

    for file in tqdm(os.listdir(src)):
        # print("Progress: " + "{:%}".format(len(chat_gpt_estimations) / (len(chat_gpt_estimations) + len(lstdir))))
        full_path = src + "/" + file
        with open(full_path) as f:
            mda_id = file.strip(".txt")
            mda_text = "\n".join(f.readlines())

            if not ai:
                lit_prop = KeywordAnalysis.analyze_mda_text(mda_text)
                try:
                    litigation_real = excel.get_litigation_for_id(mda_id)
                except Exception as e:
                    print(f"ERROR: Could not find litigation for {mda_id} in EXCEL table")
                    print(e)
                    break

                est = {"id": mda_id,
                       "litigation": lit_prop[0],
                       "probability": lit_prop[1],
                       "litigation_real": litigation_real,
                       "tokens_used": -1,
                       "long_prompt_used": -1}

                chat_gpt_estimations.append(est)
                continue

            # ai is True

            # count tokens in mda_text:
            long_prompt_used = 0

            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            # print("DEBUG: Starting decode...")
            mda_tokens = encoding.encode(mda_text)
            mda_tokens_len = len(mda_tokens)
            # print(f'DEBUG: {mda_id}.txt finished encoded in {mda_tokens_len} tokens')

            full_prompt = mda_text + PROMPT

            print("Generating response for ID: " + mda_id)

            # Wenn mda_text > TOKEN_LIMIT, dann wird der Text aufgeteilt oder gecuttet

            split_token_limit = TOKEN_LIMIT - len(
                encoding.encode(PROMPT)) - CONTENT_RESPONSE_TOKENS - MESSAGE_PRIMER_TOKENS
            if mda_tokens_len > split_token_limit:
                if cut is True:
                    long_prompt_used = 1
                    print(
                        f'WARNING: The input text is too long, \
                        cutting off the last {-(split_token_limit - mda_tokens_len)} tokens...')
                    full_prompt = encoding.decode(mda_tokens[:split_token_limit]) + PROMPT
                else:
                    long_prompt_used = 2
                    full_prompt = split_long_texts(mda_id,
                                                   mda_tokens_len,
                                                   split_token_limit,
                                                   encoding,
                                                   mda_tokens,
                                                   open_ai,
                                                   excel)

            try:
                ai_response = open_ai.send(full_prompt, excel)
            except Exception as e:
                print(f"ERROR: An error occurred while generating response for {mda_id}")
                print("ERROR occured here in line 172")
                print(e)
                break
            print(ai_response)

            try:
                ai_response_tokens = ai_response["usage"]["total_tokens"]
            except Exception as e:
                print(f"ERROR: Response format is incorrect for {mda_id}")
                print(ai_response)
                logging.exception(e)
                break
            ai_response_content = open_ai.get_response_content(ai_response)

            try:
                content_response = json.loads(ai_response_content)
                litigation = content_response["litigation"]
                probability = content_response["probability"]
            except Exception as e:
                print(f"ERROR: could not parse response content for {mda_id}")
                print(ai_response_content)
                logging.exception(e)
                litigation = -1
                probability = -1

            try:
                litigation_real = excel.get_litigation_for_id(mda_id)
            except Exception as e:
                print(f"ERROR: Could not find litigation for {mda_id} in EXCEL table")
                print(e)
                break

            est = {"id": mda_id,
                   "litigation": litigation,
                   "probability": probability,
                   "litigation_real": litigation_real,
                   "tokens_used": ai_response_tokens,
                   "long_prompt_used": long_prompt_used}

            chat_gpt_estimations.append(est)

        os.rename(full_path, res + "/" + file)

    if test is True:
        # move all files from res to src
        tmp = PATH + "/tmp"
        os.rename(src, tmp)
        os.rename(res, src)
        os.rename(tmp, res)

    # export data to excel
    print("Exporting final excel table (this may take a while)...", end="")
    excel.export_to_xlsx()
    print(" Done")

    # basic accuracy evaluation
    correct = 0
    for est in chat_gpt_estimations:
        if est["litigation"] == est["litigation_real"]:
            correct += 1

    print("Accuracy: " + "{:.1%}".format(correct / len(chat_gpt_estimations)))


def split_long_texts(mda_id, mda_tokens_len, split_token_limit, encoding, mda_tokens, open_ai, excel):
    print(f'WARNING: {mda_id}.txt is too long ({mda_tokens_len} > {split_token_limit})\n'
          f'Splitting the text into multiple parts...')
    prompt = f'Describe the content of the following text - Do not leave out any information, \
                        especially provide any numbers that are present in the text in your reply:\n\n'
    prompt_tokens = len(encoding.encode(prompt))
    final_prompt_tokens = len(encoding.encode(PROMPT))

    number_of_parts = None
    #  m = n * (T-p-((T-P-R-a)/n)-a)
    for i in itertools.count(start=1):
        if i * (
                TOKEN_LIMIT
                - prompt_tokens
                - (
                        (TOKEN_LIMIT
                         - final_prompt_tokens
                         - CONTENT_RESPONSE_TOKENS
                         - MESSAGE_PRIMER_TOKENS)
                        / i
                )
                - MESSAGE_PRIMER_TOKENS
        ) >= mda_tokens_len:
            number_of_parts = i
            break

    if number_of_parts is None:
        print("ERROR: Could not calculate number_of_parts")
        return ""
        # TODO: Error handling

    # r = (T-P-R-a)/n
    summary_max_tokens = (TOKEN_LIMIT
                          - final_prompt_tokens
                          - CONTENT_RESPONSE_TOKENS
                          - MESSAGE_PRIMER_TOKENS) / number_of_parts

    # t = T-p-r-a
    part_token_limit = math.floor(
        TOKEN_LIMIT - prompt_tokens - summary_max_tokens - MESSAGE_PRIMER_TOKENS)

    print(f'Prompt tokens: {prompt_tokens}')
    print(f'Number of parts: {number_of_parts}')
    print(f'Summary max tokens: {summary_max_tokens}')
    print(f'Part token limit: {part_token_limit}')

    summaries = []
    error_occured = False
    for part in range(number_of_parts):
        part_tokens = part * part_token_limit
        if part == number_of_parts:
            part_text = encoding.decode(mda_tokens[part_tokens:])
        else:
            part_text = encoding.decode(mda_tokens[part_tokens:part_tokens + part_token_limit])
        full_prompt = prompt + part_text
        try:
            ai_response = open_ai.send(full_prompt, excel, math.floor(summary_max_tokens))
            print(ai_response)
            summary = open_ai.get_response_content(ai_response)
            print(f'Part {part + 1}/{number_of_parts} generated successfully')
            print(summary)
            summaries.append(summary)
        except Exception as e:
            print(f"ERROR: An error occurred while generating response for {mda_id}")
            print(e)
            error_occured = True
            break
    if error_occured:
        return ""
        # TODO: Error handling
    full_prompt = " ".join(summaries) + PROMPT
    return full_prompt


if __name__ == '__main__':
    # check_too_big()
    main(ai=True, cut=True)
