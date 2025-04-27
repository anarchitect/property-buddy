import json
import os
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from datetime import datetime
from orderid import generate_unique_id

def process_function_call(function_name, arguments):
    """
    Process the function call based on the function name and arguments.
    """
    if function_name == "get_weather":
        city = arguments.get("location")
        # Example: Call a real weather API (here faked for demo)
        print(f"Calling weather API for {city}...")

        # Replace this with your real API call
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
        added_request = update_customer("unit-1", arguments)
        # service_provider_list = get_service_provider_list(category)
        
        # print(f"Service provider list: {service_provider_list}")
        # return {"confirmation_number": added_request["id"], "category": category, service_provider_list: service_provider_list}
        return {"confirmation_number": added_request["id"], "category": category}
    
    elif function_name == "get_maintenance_request_details":
        # request_id = arguments.get("request_id")
        # print(f"Checking status for maintenance request {request_id}...")
        customer_info = get_customer("unit-1")
        # return {"status": "In progress", "estimated_completion": "2023-10-15"}
        return {"response":customer_info}
    else:
        raise Exception("Unknown function")

def get_customer(customerId: str) -> str:
    url = os.environ["COSMOS_ENDPOINT"]
    client = CosmosClient(url=url, credential=DefaultAzureCredential())
    db = client.get_database_client("contoso-outdoor")
    container = db.get_container_client("customers")
    response = container.read_item(item=str(customerId), partition_key=str(customerId))
    return response

# can you follow the get_customer implementation and to create another function to update customer information by inserting a new mainteinance request into existing customer item in the database.

def get_service_provider_list(category: str) -> list:
    url = os.environ["COSMOS_ENDPOINT"]
    client = CosmosClient(url=url, credential=DefaultAzureCredential())
    db = client.get_database_client("contoso-outdoor")
    container = db.get_container_client("service-providers")

        # Retrieve the item with id "maintenance"
    maintenance_item = container.read_item(item="maintenance", partition_key="maintenance")
        # Get the list of service providers for the given category
    service_provider_list = maintenance_item.get("category", {}).get(category, [])
    return service_provider_list.get(category, [])

def update_customer(customerId: str, request: str) -> str:
    url = os.environ["COSMOS_ENDPOINT"]
    client = CosmosClient(url=url, credential=DefaultAzureCredential())
    db = client.get_database_client("contoso-outdoor")
    container = db.get_container_client("customers")
    response = container.read_item(item=str(customerId), partition_key=str(customerId))
    request_object= create_request_object(customerId, request["required_category_of_maintenance_provider"], request["description"])
    # update the customer information with the new maintenance request
    response["orders"].append(request_object)
    container.upsert_item(response)
    return request_object


def create_request_object(customer_id: str, request_type: str, description: str) -> dict:
   
    if request_type not in ["plumber", "electrician", "cleaning", "handyman"]:
        raise ValueError("Invalid request type. Must be one of: plumber, electrician, cleaning, handyman.")

    unique_id = generate_unique_id(customer_id)
    request_object = {
        "id": unique_id,
        "request_type": request_type,
        "description": description,
        "status": "pending",
        "date": datetime.utcnow().strftime("%Y-%m-%d")
    }
    return request_object
