# Wykonaj zadanie o nazwie functions zgodnie ze standardem zgłaszania odpowiedzi opisanym na tasks.aidevs.pl. Zadanie polega na zdefiniowaniu funkcji o nazwie addUser, która przyjmuje jako parametr obiekt z właściwościami: imię (name, string), nazwisko (surname, string) oraz rok urodzenia osoby (year, integer). Jako odpowiedź musisz wysłać jedynie ciało funkcji w postaci JSON-a. Jeśli nie wiesz, w jakim formacie przekazać dane, rzuć okiem na hinta: https://tasks.aidevs.pl/hint/functions
# {
#     "answer": {
#         "name": "orderPizza",
#         "description": "select pizza in pizzeria based on pizza name",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "name": {
#                     "type": "string",
#                     "description": "provide name of the pizza"
#                 }
#             }
#         }
#     }
# }
from functions.answer import answer
from functions.get_task import getTask
from functions.authenticate import authenticate
from openai import OpenAI
from dotenv import load_dotenv
import os
import json


load_dotenv()
AI_DEVS_API_URL = os.getenv('AI_DEVS_API_URL')
if AI_DEVS_API_URL is None:
    print("Please set the environment variables")
    exit()

token = authenticate('functions')

task = getTask(token)

if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)
print(task_formatted)


answer_data = {
    'answer':   {
        "name": "addUser",
                "description": "Add user to the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "User's name",
                        },
                        "surname": {
                            "type": "string",
                            "description": "User's surname",
                        },
                        "year": {
                            "type": "integer",
                            "description": "User's year of birth",
                        },
                    },
                    "required": ["name", "surname", "year"],
                },
    },
}

answer(token, answer_data)
