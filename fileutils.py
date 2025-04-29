from datetime import datetime
from azure.storage.blob import BlobServiceClient
import uuid
import os

from fastapi import File   

def upload_image(file_content) -> str:
# Configure Blob Storage
    blob_connection_string = os.environ["BLOB_CONNECTION_STRING"]
    container_name = "images"

    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Upload image
    # local_file_path = "path/to/your/image.jpg"
    blob_name = str(uuid.uuid4()) + ".jpg"  # Generate unique name

    container_client.upload_blob(name=blob_name, data=file_content)

    # Get the public URL (or SAS Token if private access)
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    print("Image URL:", blob_url)
    return blob_url

def upload_feedback(feedback, file_content) -> str:
# Configure Blob Storage
    blob_connection_string = os.environ["BLOB_CONNECTION_STRING"]
    
    container_name = "positivefeedback" if feedback == "positive" else "negativefeedback"


    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    blob_name = f"{feedback}_{timestamp}.txt"

    container_client.upload_blob(name=blob_name, data=file_content)

    # Get the public URL (or SAS Token if private access)
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    print("Feedback:", blob_url)
    return blob_url

def get_all_blobs(container_name):
        try:
            blob_connection_string = os.environ["BLOB_CONNECTION_STRING"]
            blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            blob_list = container_client.list_blobs()
            feedbacks = []
            for blob in blob_list:
                blob_data = container_client.download_blob(blob.name).readall().decode("utf-8")
                feedbacks.append({
                    "name": blob.name,
                    "content": blob_data,
                    "created_on": blob.creation_time  # capture creation time
                })
            # Sort by creation_time descending (newest first)
            feedbacks.sort(key=lambda x: x["created_on"], reverse=True)
            return feedbacks
        except Exception:
            return []