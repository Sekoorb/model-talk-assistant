from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai


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

def get_openai_response(user_input):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Define the model and prompt
    model = "gpt-3.5-turbo"
    prompt = f"User: {user_input}\nAI:"

    completion = openai.ChatCompletion.create(
    model=model,
    messages = [{"role": "user", "content": user_input}, {"role": "assistant", "content": ""}]
    )

    return completion.choices[0].message['content']

class ChatCreate(BaseModel):
    prompt: str
    reply: str

class ChatUpdate(BaseModel):
    prompt: Union[str, None] = None
    reply: Union[str, None] = None
    helpful: Union[bool, None] = None


# Define the ChatItem model
class ChatItem(BaseModel):
    id: int
    prompt: str
    reply: str
    helpful: bool


# In-memory storage for chat items
chats = []

# Route to create a new chat item
@app.post("/api/chats")
def create_chat_item(chat: ChatCreate):
    new_chat = ChatItem(id=len(chats) + 1, prompt=chat.prompt, reply=get_openai_response(chat.prompt), helpful=False)
    chats.append(new_chat)
    return new_chat

# Route to get all chat items
@app.get("/api/chats")
def get_all_chat_items():
    return chats

# Route to get a specific chat item by ID
@app.get("/api/chats/{chat_id}")
def get_chat_item(chat_id: int):
    for chat in chats:
            return chat
    return {"error": "Chat item not found"}

# Route to update a specific chat item by ID
@app.patch("/api/chats/{chat_id}")
def update_chat_item(chat_id: int, chat: ChatUpdate):
    for chat_item in chats:
        if chat_item.id == chat_id:
            chat_item.title = chat.title if chat.title is not None else chat_item.title
            chat_item.completed = chat.completed if chat.completed is not None else chat_item.completed
            return chat_item
    return {"error": "Chat item not found"}

# Route to delete a specific chat item by ID
@app.delete("/api/chats/{chat_id}")
def delete_chat_item(chat_id: int):
    for i, chat_item in enumerate(chats):
        if chat_item.id == chat_id:
            del chat_item[i]
            return {"message": "Chat item deleted"}
    return {"error": "Chat item not found"}