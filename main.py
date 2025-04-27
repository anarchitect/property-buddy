import json
import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AzureOpenAI
from fastapi.responses import FileResponse
from utils import process_function_call  # Import the function

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

# Step 2. Define available functions
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    },
    {
        "name": "create_maintenance_request",
        "description": "Send a maintenance reqeust to property manager. ",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "Description of the maintenance issue."},
                "required_category_of_maintenance_provider": {
                    "type":"string",
                    "enum": ["plumber","electrician","cleaning","handyman"],
                    "description": "The category of maintenance request to send to the property manager. which will also be used to send to relevant service provider."
                },
            },
            "required": ["description"],
        },
    },
    {
        "name": "get_maintenance_request_details",
        "description": "Get the status, estimated date, quote, and contact of the service provider of a maintenance request.",
    }
]

@app.get("/")
async def get_index():
    return FileResponse('index.html')

@app.post("/chat")
async def chat(message: HistoryMessage):

    system_message = {"role": "system", "content": "You are a helpful, concise, and professional chatbot assisting users."}
    chat_messages = [{"role": m.role, "content": m.content} for m in message.history]
    full_conversation = [system_message] + chat_messages
    final_message =""

    response = client.chat.completions.create(
        messages=full_conversation,
        functions=functions,
        function_call="auto",
        max_tokens=4096,
        temperature=1,
        top_p=1.0,
        model=os.getenv("AZURE_DEPLOYMENT_ID"))
    
    first_response = response.choices[0].message

    if first_response.function_call:
        function_name = first_response.function_call.name
        arguments = json.loads(first_response.function_call.arguments)

        # Step 6. Call the utility function to process the function call
        function_response = process_function_call(function_name, arguments)

        function_response_content = json.dumps(function_response)

        full_conversation.append({"role": first_response.role, "function_call": first_response.function_call})
        full_conversation.append({"role": "function", "name": function_name, "content": function_response_content})

        # Step 7. Send the function response back to the model
        second_response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_ID"),
            messages=full_conversation,
        )

        # Step 8. Print final model response!
        final_message = second_response.choices[0].message.content
        print("🤖 AI says:", final_message)

    else:
        # No function call, just reply
        final_message = first_response.content
        print("🤖 AI says:", final_message)

    return {"reply": final_message}
