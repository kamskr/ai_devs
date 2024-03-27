# Korzystając z modelu text-embedding-ada-002 wygeneruj embedding dla frazy Hawaiian pizza — upewnij się, że to dokładnie to zdanie. Następnie prześlij wygenerowany embedding na endpoint /answer. Konkretnie musi być to format {"answer": [0.003750941, 0.0038711438, 0.0082909055, -0.008753223, -0.02073651, -0.018862579, -0.010596331, -0.022425512, ..., -0.026950065]}. Lista musi zawierać dokładnie 1536 elementów.


import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from functions.authenticate import authenticate
from functions.get_task import getTask
from functions.answer import answer

load_dotenv()
AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')
if AI_DEVS_API_URL is None:
    print("Please set the environment variables")
    exit()

token = authenticate('embedding')

task = getTask(token)

if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

client = OpenAI()

response = client.embeddings.create(
    # input=f"{phrase}",
    input="Hawaiian pizza",
    model="text-embedding-ada-002"
)

answer_data = {
    'answer': response.data[0].embedding,
}

answer(token, answer_data)
