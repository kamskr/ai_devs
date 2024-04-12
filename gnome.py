# Rozwiąż zadanie API o nazwie ‘gnome’. Backend będzie zwracał Ci linka do obrazków przedstawiających gnomy/skrzaty. Twoim zadaniem jest przygotowanie systemu, który będzie rozpoznawał, jakiego koloru czapkę ma wygenerowana postać. Uwaga! Adres URL zmienia się po każdym pobraniu zadania i nie wszystkie podawane obrazki zawierają zdjęcie postaci w czapce. Jeśli natkniesz się na coś, co nie jest skrzatem/gnomem, odpowiedz “error”. Do tego zadania musisz użyć GPT-4V (Vision).

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from functions.authenticate import authenticate
from functions.get_task import getTask
from functions.answer import answer

load_dotenv()
AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')
if AI_DEVS_API_URL is None:
    print("Please set the environment variables")
    exit()

token = authenticate('gnome')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

print(task_formatted)

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
          "role": "user",
          "content": [
              {"type": "text", "text": "If this image represents a gnome, return ONLY the color of gnome's hat in Polish!. If it doesn't, please respond with 'error'."},
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"{task["url"]}",
                  },
              },
          ],
        }
    ],
    max_tokens=300,
)
result = response.choices[0].message.content
print(result)

answer_data = {
    'answer': result,
}

answer(token, answer_data)
