# Skorzystaj z API tasks.aidevs.pl, aby pobrać dane zadania inprompt. Znajdziesz w niej dwie właściwości — input, czyli tablicę / listę zdań na temat różnych osób (każde z nich zawiera imię jakiejś osoby) oraz question będące pytaniem na temat jednej z tych osób. Lista jest zbyt duża, aby móc ją wykorzystać w jednym zapytaniu, więc dowolną techniką odfiltruj te zdania, które zawierają wzmiankę na temat osoby wspomnianej w pytaniu. Ostatnim krokiem jest wykorzystanie odfiltrowanych danych jako kontekst na podstawie którego model ma udzielić odpowiedzi na pytanie. Zatem: pobierz listę zdań oraz pytanie, skorzystaj z LLM, aby odnaleźć w pytaniu imię, programistycznie lub z pomocą no-code odfiltruj zdania zawierające to imię. Ostatecznie spraw by model odpowiedział na pytanie, a jego odpowiedź prześlij do naszego API w obiekcie JSON zawierającym jedną właściwość “answer”.

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

token = authenticate('inprompt')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

print(task_formatted)


client = OpenAI()

question = task['question']
system_prompt = "Return just a name of the person mentioned in the question."

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{question}"}
    ]
)

name = completion.choices[0].message.content

information = [
    sentence for sentence in task['input'] if name in sentence][0]

generated_answer = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": information},
        {"role": "user", "content": f"{question}"}
    ]
)

print(generated_answer.choices[0].message.content)


answerData = {
    'answer': generated_answer.choices[0].message.content,
}
answer(token, answerData)
