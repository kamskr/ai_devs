# Rozwiąż zadanie API o nazwie ‘tools’. Celem zadania jest zdecydowanie, czy podane przez API zadanie powinno zostać dodane do listy zadań (ToDo), czy do kalendarza (jeśli ma ustaloną datę). Oba narzędzia mają lekko różniące się od siebie definicje struktury JSON-a (różnią się jednym polem). Spraw, aby Twoja aplikacja działała poprawnie na każdym zestawie danych testowych.

import json
import os

from datetime import datetime
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

token = authenticate('tools')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

print(task_formatted)
question = task['question']

# "example for ToDo": "Przypomnij mi, \u017ce mam kupi\u0107 mleko = {\"tool\":\"ToDo\",\"desc\":\"Kup mleko\" }",
# "example for Calendar": "Jutro mam spotkanie z Marianem = {\"tool\":\"Calendar\",\"desc\":\"Spotkanie z Marianem\",\"date\":\"2024-04-11\"}",
client = OpenAI()

# Todays date and day of week
current_date = datetime.now()

# Format the date as YYYY-MM-DD
formatted_date = current_date.strftime('%Y-%m-%d')
day_of_week = current_date.strftime('%A')

system_prompt = "Classify the task as ToDo or Calendar based on the input data."
tools = [
    {
        "type": "function",
        "function": {
            "name": "classify_task",
            "description": "This function is used to classify the task as ToDo or Calendar based on the input data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "enum": ["ToDo", "Calendar"],
                        "description": "The type of the tool that should be used. If date is available, the tool should be Calendar.",
                    },
                    "desc": {
                        "type": "string",
                        "description": "The description of the task that should be added to the ToDo list or Calendar.",
                    },
                    "date": {
                        "type": "string",
                        "description": f"The date when the task should be added to the Calendar. Always use YYYY-MM-DD format. Today is {formatted_date} ({day_of_week}).",
                    },
                },
                "required": ["tool", "desc"],
            },
        }
    },
]


completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system",
         "content": system_prompt},
        {"role": "user",
         "content": f"{question}"}
    ],
    tools=tools,
)

message = completion.choices[0].message
if message.tool_calls is None:
    print("No tool calls")
    print(completion)
    exit()
arguments = json.loads(message.tool_calls[0].function.arguments)
print(arguments)


answerData = {
    'answer': arguments,
}
answer(token, answerData)
