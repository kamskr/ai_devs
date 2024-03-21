import os
import requests
from functions.authenticate import authenticate
from functions.get_task import getTask
from functions.answer import answer
from dotenv import load_dotenv

load_dotenv()

url = 'https://api.openai.com/v1/moderations'
api_key = os.getenv('OPENAI_API_KEY')
token = authenticate('moderation')
task = getTask(token)

if task is None:
    print('No task available')
    exit()

sentences = task['input']


body = {
    'model': 'text-moderation-latest',
    'input': sentences,
}

response = requests.post(
    url,
    json=body,
    headers={
        'Authorization': f'Bearer {api_key}'
    },
)
print(response.json())

answers = list(
    map(lambda x: 1 if x['flagged'] else 0, response.json()['results']))

answer_json = {
    'answer': answers
}

answer(token, answer_json)
