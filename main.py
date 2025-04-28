from datetime import datetime
import json
import os
from typing import List, Optional
from fastapi import FastAPI, File, Request, UploadFile, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AzureOpenAI
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from payment_data_service import query_azure_sql
from utils import get_property, process_function_call  # Import the function
from fileutils import upload_image  # Import the function
from function_call_specs import functions  # Import the functions list

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

def handle_function_call_response(client, first_response, function_response, full_conversation, function_name):
    function_response_content = json.dumps(function_response)
    print (f"Function response content: {function_response_content}")
    full_conversation.append({"role": first_response.role, "function_call": first_response.function_call})
    full_conversation.append({"role": "function", "name": function_name, "content": function_response_content})

    # Step 7. Send the function response back to the model
    second_response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_ID"),
        messages=full_conversation,
    )
    final_message = second_response.choices[0].message.content
    return final_message

@app.get("/")
async def get_index():
    return FileResponse('index.html')

@app.get("/myrequests", response_class=HTMLResponse)
async def show_profile(request: Request):
    templates = Jinja2Templates(directory="templates")
    property_id = os.environ["PROPERTY_ID"]
    items = get_property(property_id)
    if not items:
        return HTMLResponse(content="No resident found.", status_code=404)

    resident = items[0]

    return templates.TemplateResponse(
        "resident_profile.html",
        {"request": request, "resident": resident}
    )

@app.get("/mypayments", response_class=HTMLResponse)
async def get_payments(request: Request):
    customer_id = os.environ["PROPERTY_ID"]
    templates = Jinja2Templates(directory="templates")
    sql = "SELECT amount, due_date, payee, payment_type, status FROM payment WHERE customer_id = {customer_id} ORDER BY due_date ASC;"
    sql_with_customer_id = sql.format(customer_id=f"'{customer_id}'")
    print(f"Getting payment information for {sql_with_customer_id}...")
    payments = query_azure_sql(sql_with_customer_id)
    payments_json = json.loads(payments)
    for payment in payments_json:
        payment['amount'] = float(payment['amount'])
    return templates.TemplateResponse(
        "payment_list.html",
        {"request": request, "customer_id": customer_id, "payments": payments_json}
    )


@app.post("/chat_with_upload/")
async def chat_with_upload(
    message: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Endpoint to handle chat messages and optional file uploads.
    """
    response_data = {}

    message_dict = json.loads(message)
    chat_history = HistoryMessage(**message_dict)

    # Handle chat message
    if chat_history:
        system_message = {"role": "system", "content": "You are a helpful, concise, and professional chatbot assisting users."}
        chat_messages = [{"role": m.role, "content": m.content} for m in chat_history.history]
        full_conversation = [system_message] + chat_messages

        response = client.chat.completions.create(
            messages=full_conversation,
            functions=functions,
            function_call="auto",
            max_tokens=4096,
            temperature=1,
            top_p=1.0,
            model=os.getenv("AZURE_DEPLOYMENT_ID")
        )

        first_response = response.choices[0].message
        if first_response.function_call:
            function_name = first_response.function_call.name
            arguments = json.loads(first_response.function_call.arguments)
            file_contents = await file.read() if file else None
            function_response = process_function_call(function_name, arguments,file_contents)
            final_message = handle_function_call_response(client, first_response, function_response, full_conversation, function_name)
            response_data["chat_reply"] = final_message 
            # //json.dumps(final_message)
        else:
            response_data["chat_reply"] = first_response.content

    # # Handle file upload
    # if file:
    #     contents = await file.read()
    #     response_data["file_upload"] = {
    #         "filename": file.filename,
    #         "content_type": file.content_type,
    #         "size": len(contents)
    #     }

    return response_data

@app.post("/feedback")
async def feedback(user_message: str = Form(...), response_text: str = Form(...), feedback: str = Form(...)):
    os.makedirs('user_feedback', exist_ok=True)

    filename = "positive_results.txt" if feedback == "positive" else "negative_results.txt"
    filepath = os.path.join("user_feedback", filename)

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"Feedback received at: {timestamp}\n")
        f.write(f"User: {user_message}\n")
        f.write(f"Assistant: {response_text}\n")
        f.write("-" * 50 + "\n")

    return {"status": "ok"}