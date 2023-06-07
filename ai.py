import logging
import time
import openai
from globals import CONTENT_RESPONSE_TOKENS, API_KEY, API_BASE, CONNECTION_LOSS_TIMEOUT


class Ai:

    def __init__(self):
        openai.api_key = API_KEY
        openai.api_base = API_BASE
        print("OpenAI initialized")
        self.initialized = True

    def send(self, prompt, excel, max_tokens=CONTENT_RESPONSE_TOKENS):
        if not self.initialized:
            print("ai not initialized")
            exit(1)
        ai_response = None
        try:
            ai_response = openai.Completion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "user", "content": prompt}],
                                                   temperature=0,
                                                   max_tokens=max_tokens)
        except openai.error.APIConnectionError as e:
            print(e)
            print("ERROR: APIConnectionError: Waiting for Internet connection...")
            # excel.export_to_csv()
            excel.export_to_xlsx()

            # while loop to wait for internet connection
            while True:
                try:
                    time.sleep(CONNECTION_LOSS_TIMEOUT)
                    ai_response = openai.Completion.create(model="gpt-3.5-turbo",
                                                           messages=[{"role": "user", "content": prompt}],
                                                           temperature=0,
                                                           max_tokens=max_tokens)
                    break
                except openai.error.APIConnectionError:
                    continue
        if ai_response is None:
            print("ai_response is None")
            exit(1)
        return ai_response

    @staticmethod
    def get_response_content(ai_response):
        try:
            return ai_response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"ERROR: Response format is incorrect")
            print(ai_response)
            logging.exception(e)
