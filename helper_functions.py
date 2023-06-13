import os
import tiktoken

from globals import TOKEN_LIMIT, PROMPT, CONTENT_RESPONSE_TOKENS, path


def check_too_big():
    too_long_texts = 0
    src = path + "src"
    for file in os.listdir(src):
        full_path = src + "/" + file
        with open(full_path) as f:
            mda_text = "\n".join(f.readlines())

            # count tokens in mda_text:

            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            mda_tokens = encoding.encode(mda_text)
            mda_tokens_len = len(mda_tokens)

            split_token_limit = TOKEN_LIMIT - len(encoding.encode(PROMPT)) - CONTENT_RESPONSE_TOKENS
            if mda_tokens_len > split_token_limit:
                too_long_texts += 1

    print(f'There are {too_long_texts} texts that are too long')


def find_missing_files():
    src = path + "src"
    freytag_path = path + "hans"
    missing_files_txt = "fehlende_mda.txt"
    with open(missing_files_txt) as missing_files:
        for missing_file in missing_files.readlines():
            missing_file = missing_file.strip()
            os.rename(f'{freytag_path}/{missing_file}.txt', f'{src}/{missing_file}.txt')
