# Wykonaj zadanie API o nazwie ‘knowledge’. Automat zada Ci losowe pytanie na temat kursu walut, populacji wybranego kraju lub wiedzy ogólnej. Twoim zadaniem jest wybór odpowiedniego narzędzia do udzielenia odpowiedzi (API z wiedzą lub skorzystanie z wiedzy modelu). W treści zadania uzyskanego przez API, zawarte są dwa API, które mogą być dla Ciebie użyteczne.

import json
import os
import requests

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

token = authenticate('knowledge')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

# print(task_formatted)


client = OpenAI()


def get_currency_rate(currency):
    url = f"http://api.nbp.pl/api/exchangerates/rates/a/{
        currency}/?format=json"
    response = requests.get(url)
    return response.json()['rates'][0]['mid']


def get_country_population(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)
    return response.json()[0]['population']


def general_knowledge(question):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": system_prompt},
            {"role": "user",
             "content": f"{question}"}
        ],
    )
    print(completion)
    return completion.choices[0].message.content


question = task['question']
print(question)
system_prompt = "Answer with function calling, based on the question"

completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{question}"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_currency_rate",
                "description": "This function is used to get the current rate for given currency.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "currency": {
                            "type": "string",
                            "description": "The 3-letter currency code to get the rate for, e.g. usd, eur",
                        },
                    },
                    "required": ["currency"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_country_population",
                "description": "This function is used to get the population of a given country.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country": {
                            "type": "string",
                            "description": "The name of the country to get the population for. This name has to be in English, lowercase, e.g. poland, germany, france",
                        },
                    },
                    "required": ["country"]
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "general_knowledge",
                "description": "This function is used to get an answer to a general knowledge question.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The question to get the answer for.",
                        },
                    },
                    "required": ["question"]
                },
            }
        },
    ]

)
#

message = completion.choices[0].message
if message.tool_calls is None:
    print("No tool calls")
    exit()


function_name = message.tool_calls[0].function.name

arguments = json.loads(message.tool_calls[0].function.arguments)

final_answer = None

if (function_name == 'get_currency_rate'):
    currency = arguments['currency']
    final_answer = get_currency_rate(currency)
elif (function_name == 'get_country_population'):
    country = arguments['country']
    final_answer = get_country_population(country)
elif (function_name == 'general_knowledge'):
    question = arguments['question']
    final_answer = general_knowledge(question)


#
answerData = {
    'answer': final_answer,
}
answer(token, answerData)
