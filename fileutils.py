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
