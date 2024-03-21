import os
import requests
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

body = {
    'model': 'gpt-3.5-turbo',
    "messages": [
        {
            "role": "system",
            "content": "You are a blogger. You are writing a blog posts " +
            "about provided topics. You will be given an array of topis. " +
            "You need to respond with the blog post about pizza that fits " +
            "to the given topics. Generated articles should be returned as " +
            "a string in an array. Example: input = '['topic1', 'tipic2']' " +
            "result: '['article about topic1', 'aricle about topic2']'" +
            "You should write full articles about the topics." +
            "You should only answer with the articles inside the array."

        },
        {
            "role": "user",
            "content": f"{topics}"
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
    'answer': articles
}

print()

# answer(token, answer_body)
