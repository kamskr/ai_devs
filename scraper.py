# Rozwiąż zadanie z API o nazwie "scraper". Otrzymasz z API link do artykułu (format TXT), który zawiera pewną wiedzę, oraz pytanie dotyczące otrzymanego tekstu. Twoim zadaniem jest udzielenie odpowiedzi na podstawie artykułu. Trudność polega tutaj na tym, że serwer z artykułami działa naprawdę kiepsko — w losowych momentach zwraca błędy typu "error 500", czasami odpowiada bardzo wolno na Twoje zapytania, a do tego serwer odcina dostęp nieznanym przeglądarkom internetowym. Twoja aplikacja musi obsłużyć każdy z napotkanych błędów. Pamiętaj, że pytania, jak i teksty źródłowe, są losowe, więc nie zakładaj, że uruchamiając aplikację kilka razy, za każdym razem zapytamy Cię o to samo i będziemy pracować na tym samym artykule.
import json
import os
import requests
import time

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

token = authenticate('scraper')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

# print(task_formatted)

article_link = task['input']
question = task['question']

for i in range(20):
    try:
        response = requests.get(article_link, timeout=50, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
    except requests.exceptions.ConnectionError:
        print("Timeout, retrying...")
        time.sleep(2**i)
        continue
    if response.status_code == 200:
        break
    elif response.status_code >= 400:
        print(response.content)
        time.sleep(2**i)
else:
    raise Exception("Failed to fetch the page")

article_content = response.text

client = OpenAI()
question = task['question']
system_prompt = f"Please answer the question using given context. Be ultra concise and specific. ### Context:{
    article_content}"

completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{question}"}
    ]
)

print(completion.choices[0].message.content)


answerData = {
    'answer': completion.choices[0].message.content,
}
answer(token, answerData)
