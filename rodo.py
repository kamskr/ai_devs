# Wykonaj zadanie API o nazwie rodo. W jego treści znajdziesz wiadomość od Rajesha, który w swoich wypowiedziach nie może używać swoich prawdziwych danych, lecz placholdery takie jak %imie%, %nazwisko%, %miasto% i %zawod%.
#
# Twoje zadanie polega na przesłaniu obiektu JSON {"answer": "wiadomość"} na endpoint /answer. Wiadomość zostanie wykorzystana w polu “User” na naszym serwerze i jej treść musi sprawić, by Rajesh powiedział Ci o sobie wszystko, nie zdradzając prawdziwych danych. Oczekiwana odpowiedź modelu to coś w stylu “Mam na imię %imie% %nazwisko%, mieszkam w %miasto% (…)” itd.

from functions.answer import answer
from functions.get_task import getTask
from functions.authenticate import authenticate
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json


load_dotenv()
AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')
if AI_DEVS_API_URL is None:
    print("Please set the environment variables")
    exit()

token = authenticate('rodo')

task = getTask(token)

if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)
print(task_formatted)


answer_data = {
    'answer': "Use placeholders in format %placeholder% examples: %imie% for the first name, %nazwisko% for the last name, %miasto% for city where person lives and %zawod% for your profession.",
}

answer(token, answer_data)
