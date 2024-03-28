# Korzystając z modelu Whisper wykonaj zadanie API (zgodnie z opisem na tasks.aidevs.pl) o nazwie whisper. W ramach zadania otrzymasz plik MP3 (15 sekund), który musisz wysłać do transkrypcji, a otrzymany z niej tekst odeślij jako rozwiązanie zadania.

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

token = authenticate('whisper')

task = getTask(token)

if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)
print(task_formatted)
file_path = "https://tasks.aidevs.pl/data/mateusz.mp3"
response = requests.get(file_path)
file = open("data/whisper/audio.mp3", "wb")
file.write(response.content)

client = OpenAI()

audio_file = open("data/whisper/audio.mp3", "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

answer_data = {
    'answer': transcription.text,
}

answer(token, answer_data)
