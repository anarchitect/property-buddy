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
    }
]

def dispatch(function_name, arguments):
    if function_name == "get_weather":
        city = arguments.get("location")
        # Example: Call a real weather API (here faked for demo)
        print(f"Calling weather API for {city}...")

        # 🔥 Replace this with your real API call
        weather_result = {
            "location": city,
            "temperature_celsius": 22,
            "condition": "Partly cloudy"
        }
        return weather_result
    elif function_name == "create_maintenance_request":
        description = arguments.get("description")
        category = arguments.get("required_category_of_maintenance_provider")
        print(f"Creating maintenance request for {description}...")
        print(f"Category: {category}")
        # Example: Call a real maintenance request API (here faked for demo)    
        return {"confirmation_number": "XYZ789", "service_provider": category}
    else:
        raise Exception("Unknown function")


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

        # Step 6. Call your real API based on function name
        function_response = dispatch(function_name, arguments)    

        function_response_content = json.dumps(function_response)

        full_conversation.append({"role":first_response.role,"function_call":first_response.function_call})       # the model’s function_call message
# append this object to full_conversation
        full_conversation.append({"role": "function", "name": function_name, "content": function_response_content})  # the function response


        # Step 7. Send the function response back to the model
        second_response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_ID"),
            messages=full_conversation,  # original user message
        )

        # Step 8. Print final model response!
        final_message = second_response.choices[0].message.content
        print("🤖 AI says:", final_message)

    else:
        # No function call, just reply
        final_message = first_response.content
        print("🤖 AI says:", final_message)

    return {"reply": final_message}
