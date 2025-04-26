import os
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

class Message(BaseModel):
    user_message: str

@app.get("/")
async def get_index():
    return FileResponse('index.html')

@app.post("/chat")
async def chat(message: Message):
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": message.user_message
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=os.getenv("AZURE_DEPLOYMENT_ID"),
)
    return {"reply": response.choices[0].message.content}
