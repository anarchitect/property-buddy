import json
import os
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

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
        return {"confirmation_number": "XYZ789", "service_provider": category}
    
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