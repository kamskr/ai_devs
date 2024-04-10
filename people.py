# Rozwiąż zadanie o nazwie “people”. Pobierz, a następnie zoptymalizuj odpowiednio pod swoje potrzeby bazę danych https://tasks.aidevs.pl/data/people.json. Twoim zadaniem jest odpowiedź na pytanie zadane przez system. Uwaga! Pytanie losuje się za każdym razem na nowo, gdy odwołujesz się do /task. Spraw, aby Twoje rozwiązanie działało za każdym razem, a także, aby zużywało możliwie mało tokenów. Zastanów się, czy wszystkie operacje muszą być wykonywane przez LLM-a - może warto zachować jakiś balans między światem kodu i AI?
import json
import os
import re
from fuzzywuzzy import process
from openai import OpenAI
from dotenv import load_dotenv
import requests
from functions.authenticate import authenticate
from functions.get_task import getTask
from functions.answer import answer

load_dotenv()
AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')
if AI_DEVS_API_URL is None:
    print("Please set the environment variables")
    exit()

token = authenticate('people')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

print(task_formatted)
url = "https://tasks.aidevs.pl/data/people.json"
people = requests.get(url).json()

name_surname_list = []
for person in people:
    name_surname_list.append(person['imie'] + ' ' + person['nazwisko'])

question = task['question']

# Regular expression to match the name and surname structure, assuming standard Polish naming conventions
# This pattern aims to capture common Polish names and surnames, considering potential name inflections
pattern = r"\b[A-ZŁŚ][a-ząęółśżźćń]+ [A-ZŁŚ][a-ząęółśżźćń]+"

# Searching for the pattern in the question
match = re.search(pattern, question)

# Extracting the name and surname if found
searched_name = match.group(0) if match else "Name not found"

closest_match = process.extractOne(searched_name, name_surname_list)

person = None

for p in people:
    if p["imie"] in closest_match[0] and p['nazwisko'] in closest_match[0]:
        person = p
        break

open_ai = OpenAI()


def json_to_markdown(json_obj):
    markdown = ""
    for key, value in json_obj.items():
        markdown += f"- **{key}**: {value}\n"
    return markdown


context = json_to_markdown(person)
print(context)
completion = open_ai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"{context}", },
        {"role": "user", "content": f"{question}"}
    ]
)

result = completion.choices[0].message.content

print(completion)


answer_data = {
    'answer': result,
}

answer(token, answer_data)
