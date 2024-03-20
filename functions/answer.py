
import requests
import os
from dotenv import load_dotenv


def answer(token, answer):
    load_dotenv()
    AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')

    if AI_DEVS_API_URL is None:
        print("Please set the environment variables")
        return

    response = requests.post(
        AI_DEVS_API_URL + f'/answer/{token}', json=answer)

    if response.status_code == 200:
        print("Answer submitted successfully")
    else:
        print("Answer submission failed")
        print(response.text)
