# Rozwiąż zadanie o nazwie “whoami”. Za każdym razem, gdy pobierzesz zadanie, system zwróci Ci jedną ciekawostkę na temat pewnej osoby. Twoim zadaniem jest zbudowanie mechanizmu, który odgadnie, co to za osoba. W zadaniu chodzi o utrzymanie wątku w konwersacji z backendem. Jest to dodatkowo utrudnione przez fakt, że token ważny jest tylko 2 sekundy (trzeba go cyklicznie odświeżać!). Celem zadania jest napisania mechanizmu, który odpowiada, czy na podstawie otrzymanych hintów jest w stanie powiedzieć, czy wie, kim jest tajemnicza postać. Jeśli odpowiedź brzmi NIE, to pobierasz kolejną wskazówkę i doklejasz ją do bieżącego wątku. Jeśli odpowiedź brzmi TAK, to zgłaszasz ją do /answer/. Wybraliśmy dość ‘ikoniczną’ postać, więc model powinien zgadnąć, o kogo chodzi, po maksymalnie 5-6 podpowiedziach. Zaprogramuj mechanizm tak, aby wysyłał dane do /answer/ tylko, gdy jest absolutnie pewny swojej odpowiedzi.

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

memory = "###Context"
client = OpenAI()
prompt = "Tell me who the person is, given the information inside context. Only aswer if you are CERTAIN who the person is. If you are not sure, or need more information, return single word 'hint'"


def get_hint():
    token = authenticate('whoami')
    task = getTask(token)
    if task is None:
        print('No task available')
        exit()
    hint = task['hint']
    context = memory + "\n" + hint
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )
    guess = completion.choices[0].message.content

    return token, context, guess


for i in range(10):
    [token, context, guess] = get_hint()
    memory = context
    if guess == "hint":
        continue

    answerData = {
        'answer': guess,
    }
    answer(token, answerData)
    break
