from typing import Union
<<<<<<< HEAD

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
=======
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import openai
import time
import os
>>>>>>> d7a1d41926f4c65238a6481e61978ee1d030278e

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Load the .env file
load_dotenv()

# Load the .env file at the beginning, to make sure the OPENAI_API_KEY is loaded
openai.api_key = os.getenv("OPENAI_API_KEY")

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

<<<<<<< HEAD

class TodoCreate(BaseModel):
    title: str

=======
class ChatCreate(BaseModel):
    prompt: str
>>>>>>> d7a1d41926f4c65238a6481e61978ee1d030278e

class TodoUpdate(BaseModel):
    title: Union[str, None] = None
    completed: Union[bool, None] = None


# Define the TodoItem model
class TodoItem(BaseModel):
    id: int
<<<<<<< HEAD
    title: str
    completed: bool

=======
    prompt: str
    reply: str
>>>>>>> d7a1d41926f4c65238a6481e61978ee1d030278e

# In-memory storage for todo items
todos = []

<<<<<<< HEAD
# Route to create a new todo item
@app.post("/api/todos")
def create_todo_item(todo: TodoCreate):
    new_todo = TodoItem(id=len(todos) + 1, title=todo.title, completed=False)
    todos.append(new_todo)
    return new_todo

# Route to get all todo items
@app.get("/api/todos")
def get_all_todo_items():
    return todos

# Route to get a specific todo item by ID
@app.get("/api/todos/{todo_id}")
def get_todo_item(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error": "Todo item not found"}

# Route to update a specific todo item by ID
@app.patch("/api/todos/{todo_id}")
def update_todo_item(todo_id: int, todo: TodoUpdate):
    for todo_item in todos:
        if todo_item.id == todo_id:
            todo_item.title = todo.title if todo.title is not None else todo_item.title
            todo_item.completed = todo.completed if todo.completed is not None else todo_item.completed
            return todo_item
    return {"error": "Todo item not found"}

# Route to delete a specific todo item by ID
@app.delete("/api/todos/{todo_id}")
def delete_todo_item(todo_id: int):
    for i, todo_item in enumerate(todos):
        if todo_item.id == todo_id:
            del todos[i]
            return {"message": "Todo item deleted"}
    return {"error": "Todo item not found"}
=======
def get_openai_stream(prompt: str):
    openai_stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        stream=True,
    )
    try:
        for event in openai_stream:
            if "content" in event["choices"][0].delta:
                current_response = event["choices"][0].delta.content
                yield "data: " + current_response + "\n\n"
                time.sleep(0.1)
    except Exception as e:
        print("Stream encountered an error:", e)
    finally:
        yield "event: end-of-stream\ndata: \n\n"  # Signal the end of the stream

@app.get("/api/stream")
def stream(prompt: str):
    #response.headers['Cache-Control'] = 'no-cache'
    return StreamingResponse(get_openai_stream(prompt), media_type='text/event-stream')

# Route to get all chat items
@app.get("/api/chats")
async def get_all_chat_items():
    return chats
>>>>>>> d7a1d41926f4c65238a6481e61978ee1d030278e
