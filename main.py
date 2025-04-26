import json
import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AzureOpenAI
from fastapi.responses import FileResponse

# Load .env file
load_dotenv()

# FastAPI app
app = FastAPI()

client = AzureOpenAI(
    api_version=os.getenv("OPEN_API_VERSION"),
    azure_endpoint=os.getenv("OPEN_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

class MessageEntry(BaseModel):
    role: str
    content: str

class HistoryMessage(BaseModel):
    history: List[MessageEntry]

@app.get("/")
async def get_index():
    return FileResponse('index.html')

@app.post("/chat")
async def chat(message: HistoryMessage):

    system_message = {"role": "system", "content": "You are a helpful, concise, and professional chatbot assisting users."}
    chat_messages = [{"role": m.role, "content": m.content} for m in message.history]
    full_conversation = [system_message] + chat_messages

# combine system message with message, which is a HistoryMessage into a new single list

    response = client.chat.completions.create(
    messages=full_conversation,
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=os.getenv("AZURE_DEPLOYMENT_ID"),
)
    return {"reply": response.choices[0].message.content}
