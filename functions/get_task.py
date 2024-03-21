
import requests
import os
from dotenv import load_dotenv


def getTask(token):
    load_dotenv()
    AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')

    if AI_DEVS_API_URL is None:
        print("Please set the environment variables")
        return

    response = requests.get(
        AI_DEVS_API_URL + f'/task/{token}')

    if response.status_code == 200:
        return response.json()
    else:
        print("Task retrieval failed")
        print(response.text)
