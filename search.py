# Dziś zadanie jest proste, ale nie łatwe — zaimportuj do swojej bazy wektorowej, spis linków z newslettera unknowNews z adresu:
# https://unknow.news/archiwum_aidevs.json
# [to mały wycinek bazy, jeśli chcesz pobrać całą bazę, to użyj pliku archiwum.json]

import json
import os
import uuid
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
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

token = authenticate('search')

task = getTask(token)
if task is None:
    print('No task available')
    exit()

task_formatted = json.dumps(task, indent=2)

print(task_formatted)
uknown_news_url = "https://unknow.news/archiwum_aidevs.json"
unknown_news = requests.get(uknown_news_url).json()


collection_name = "unknown_news"

qdrant = QdrantClient(url="http://localhost:6333")

existing_collections = qdrant.get_collections().collections

# Check if collection exists
indexed = next(
    (collection for collection in existing_collections if collection.name == collection_name), None)

if indexed is None:
    indexed = qdrant.create_collection(collection_name=collection_name,
                                       vectors_config=VectorParams(size=1536, distance=Distance.COSINE),)

open_ai = OpenAI()

# Index all data
# points = []
# for news in unknown_news:
#     title = news['title']
#     info = news['info']
#     url = news['url']
#     id = str(uuid.uuid4())
#     content = f"# {title}\n{info}"
#     metadata = {
#         "url": url,
#         "title": title,
#         "id": id
#     }
#     # Create embeddings
#     response = open_ai.embeddings.create(
#         input=content,
#         model="text-embedding-ada-002"
#     )
#     embedding = response.data[0].embedding
#     point = PointStruct(id=id, vector=embedding, payload=metadata)
#     print(point)
#     points.append(point)
#
#
# qdrant.upsert(collection_name=collection_name,
#               wait=True,
#               points=points)

question = task['question']
print(question)

response = open_ai.embeddings.create(
    input=question,
    model="text-embedding-ada-002"
)
question_embedding = response.data[0].embedding

search_result = qdrant.search(
    collection_name=collection_name,  query_vector=question_embedding, limit=1)

url = search_result[0].payload['url']

answer_data = {
    'answer': url,
}

answer(token, answer_data)
