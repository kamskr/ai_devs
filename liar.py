# API: wykonaj zadanie o nazwie liar. Jest to mechanizm, który mówi nie na temat w 1/3 przypadków. Twoje zadanie polega na tym, aby do endpointa /task/ wysłać swoje pytanie w języku angielskim (dowolne, np “What is capital of Poland?’) w polu o nazwie ‘question’ (metoda POST, jako zwykłe pole formularza, NIE JSON). System API odpowie na to pytanie (w polu ‘answer’) lub zacznie opowiadać o czymś zupełnie innym, zmieniając temat. Twoim zadaniem jest napisanie systemu filtrującego (Guardrails), który określi (YES/NO), czy odpowiedź jest na temat. Następnie swój werdykt zwróć do systemu sprawdzającego jako pojedyncze słowo YES/NO. Jeśli pobierzesz treść zadania przez API bez wysyłania żadnych dodatkowych parametrów, otrzymasz komplet podpowiedzi. Skąd wiedzieć, czy odpowiedź jest ‘na temat’? Jeśli Twoje pytanie dotyczyło stolicy Polski, a w odpowiedzi otrzymasz spis zabytków w Rzymie, to odpowiedź, którą należy wysłać do API to NO.


from openai import OpenAI
import json
import requests
import os
from dotenv import load_dotenv

from functions.authenticate import authenticate
from functions.get_task import getTask
from functions.answer import answer

load_dotenv()
token = authenticate('liar')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

print(task_formatted)

AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')

if AI_DEVS_API_URL is None:
    print("Please set the environment variables")
    exit()

question = 'What is the capital of Poland?'

form_data = {
    'question': question
}

response = requests.post(
    AI_DEVS_API_URL + f'/task/{token}', data=form_data)


generated_answer = response.json()['answer']

client = OpenAI()

system_prompt = "Verify it the answer is correct. " + \
    "If answer is correct, send YES, if not, send NO."

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user",
            "content": f"Question: {question}," +
         f"Answer: {generated_answer}"}
    ]
)

result = completion.choices[0].message.content

answer_data = {
    'answer': result
}


answer(token, answer_data)
