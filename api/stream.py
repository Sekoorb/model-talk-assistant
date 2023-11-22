'''
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import time
from dotenv import load_dotenv
import os

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

@app.get("/api/healthchecker")
def healthchecker():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "can you type 1 2 3 4 3 2 1?"

def get_openai_generator(prompt: str):
    openai_stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        stream=True,
    )
    for event in openai_stream:
        if "content" in event["choices"][0].delta:
            current_response = event["choices"][0].delta.content
            yield "data: " + current_response + "\n\n"

@app.get('/api/stream')
async def stream():
    return StreamingResponse(get_openai_generator(prompt), media_type='text/event-stream')

import requests

url = "http://127.0.0.1:3000/api/stream/"

with requests.get(url, stream=True) as r:
    for chunk in r.iter_content(None, decode_unicode=True):
        if chunk:
            print(chunk, end='', flush=True)
'''