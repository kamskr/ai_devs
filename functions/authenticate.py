import requests
import os
from dotenv import load_dotenv


def authenticate(taskName):
    load_dotenv()
    AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')
    AI_DEVS_API_KEY = os.getenv('AI_DEVS_API_KEY')

    if AI_DEVS_API_URL is None or AI_DEVS_API_KEY is None:
        print("Please set the environment variables")
        return

    data = {'apikey': AI_DEVS_API_KEY}

    response = requests.post(
        AI_DEVS_API_URL + f'/token/{taskName}', json=data)

    if response.status_code == 200:
        return response.json()['token']
    else:
        print("Authentication failed")
        print(response.text)
