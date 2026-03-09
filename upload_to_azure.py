from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import os

# Paste your connection string here
AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=ayushgenai;AccountKey=pBgwLfRbp1SVxd/tHM65HMDcYCkT54SEuhLmirR5m6IcIQ/gAdSNJ0YpbNNV/q16G38V+FuxyS/x+AStj2wV7Q==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "audit-log-raw"
FILE_NAME = "business_audit_logs.csv"

def upload_to_blob():
    try:
        print("Connecting to Azure...")
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # --- NEW STEP: Automatically create the container if it is missing ---
        try:
            container_client.create_container()
            print(f"Created new container: '{CONTAINER_NAME}'")
        except ResourceExistsError:
            print(f"Container '{CONTAINER_NAME}' already exists. Proceeding...")
        # ---------------------------------------------------------------------
        
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=FILE_NAME)
        
        print(f"Uploading {FILE_NAME} to Azure Blob Storage...")
        with open(FILE_NAME, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            
        print("Upload successful! Your data is now in the cloud.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_to_blob()