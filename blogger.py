import os
import requests
import json
from functions.authenticate import authenticate
from functions.get_task import getTask
from functions.answer import answer
from dotenv import load_dotenv

load_dotenv()

url = 'https://api.openai.com/v1/chat/completions'
api_key = os.getenv('OPENAI_API_KEY')
token = authenticate('blogger')
task = getTask(token)

if task is None:
    print('No task available')
    exit()

topics = task['blog']
print(topics)

file = open('prompts/blogger.txt', 'r')
system = file.read()

file.close()


body = {
    'model': 'gpt-4',
    "messages": [
        {
            "role": "system",
            "content": system,
        },
        {
            "role": "user",
            "content": f"only with an array of articles {topics}"
        }
    ]
}

response = requests.post(
    url,
    json=body,
    headers={
        'Authorization': f'Bearer {api_key}'
    },
)

articles = response.json()['choices'][0]['message']['content']


print(articles)

answer_body = {
    'answer': json.loads(articles)
}


answer(token, answer_body)
