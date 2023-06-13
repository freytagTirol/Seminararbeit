import os
from dotenv import load_dotenv

if load_dotenv():
    API_BASE = os.getenv("API_BASE")
    API_KEY = os.getenv("API_KEY")
else:
    API_BASE = "https://api.openai.com/v1/chat/"
    API_KEY = None

PROMPT = "\n\
        \n\
        how likely is it that the company faces future litigation after submitting the above-mentioned md&a in form\
        10-k? respond only in json format, like \'{\"litigation\":1, \"probability\":5}\' \
        litigation should be either 1 (indicating litigation) or 0 (no litigation). \
        probability should be a number between 1 and 5 with 1 indicating low likelihood of litigation and 5 \
        indicating the highest likelihood of litigation."

# path = "C:/Users/frotz/Desktop/Freiburg VWL/Skripte/Semester 4/Seminar/Files/MDA_test/"

CONNECTION_LOSS_TIMEOUT = 5

TOKEN_LIMIT = 4096

CONTENT_RESPONSE_TOKENS = 11

# MESSAGE_PRIMER = '"role": "user", "content"' # TODO: Why is this 9?? in reality it's 8 (actual sent tokens)
MESSAGE_PRIMER_TOKENS = 8
