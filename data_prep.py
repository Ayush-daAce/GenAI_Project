import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

# --- 1. DOWNLOAD RAW DATA FROM AZURE ---
AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=ayushgenai;AccountKey=pBgwLfRbp1SVxd/tHM65HMDcYCkT54SEuhLmirR5m6IcIQ/gAdSNJ0YpbNNV/q16G38V+FuxyS/x+AStj2wV7Q==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "audit-log-raw"
FILE_NAME = "business_audit_logs.csv"
DOWNLOAD_PATH = "downloaded_audit_logs.csv"

print("Downloading raw data from Azure Blob Storage...")
try:
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=FILE_NAME)
    with open(DOWNLOAD_PATH, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    print("Download complete!")
except Exception as e:
    print(f"Azure download failed: {e}")
    exit()

# --- 2. PANDAS DATA TRANSFORMATION ---
print("Starting Pandas Data Processing...")

# Load the downloaded dataset
df = pd.read_csv(DOWNLOAD_PATH)

# Clean: Drop any rows where the auditor note is missing
df_clean = df.dropna(subset=["Auditor_Notes"])

# Transform: Create a highly contextual string for the LLM
# We use apply to concatenate the columns into a rich text sentence row by row
df_clean["LLM_Context"] = df_clean.apply(
    lambda row: f"On {row['Audit_Date']}, the {row['Department']} department (Risk Level: {row['Risk_Level']}, "
                f"Financial Impact: ${row['Financial_Impact_USD']}) reported the following audit note: {row['Auditor_Notes']}", 
    axis=1
)

# Save the output to a text file ready for LangChain
OUTPUT_FILE = "cleaned_llm_data.txt"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for item in df_clean["LLM_Context"]:
        f.write(f"{item}\n\n")

print(f"Success! Data transformed and saved to '{OUTPUT_FILE}'.")