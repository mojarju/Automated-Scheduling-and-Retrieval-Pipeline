"""
lambda_function.py

Short description of what this script does.

Author: Momodou (Mo) Jarju
Date: 2026-May-2
"""

# Import Libraries required to run this script 
import os 
import json 
import boto3
import pandas as pd 
import requests
from io import StringIO
import logging 
import datetime

# Setup logging
logger = logging.getLogger() # will show every level except DEBUG
logger.setLevel(logging.INFO)

# -----------------------------
# Constants
# -----------------------------
# Environment Variables (Configured in Lambda)
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'pvh-kareem')      # //FIXME: - update the s3 bucket name 
S3_FOLDER_PATH = os.getenv('S3_FOLDER_PATH', 'calendly/')
SECRET_NAME = os.getenv('CALENDLY_SECRET_NAME', 'calendly-api-key')
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1') 

# Initialize AWS Clients
secrets_client = boto3.client('secretsmanager', region_name=REGION_NAME)
s3_client = boto3.client('s3')

# Generate Timestamp for File Naming 
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
S3_CALANDY_PATH = f"{S3_FOLDER_PATH}calandy_scheduled_calls_{timestamp}.csv"
S3_METRICS_PATH = f"{S3_FOLDER_PATH}campaign_metrics_{timestamp}.csv"

# -----------------------------
# Functions
# -----------------------------
def get_calendy_api_key():
    """Fetch the Calendy API Key from Secrets Manager."""
    try:
        response = secrets_client.get_sectet_value(SecretId=SECRET_NAME)
        secret = json.loads(response["SecretString"])
        return secret.get('calendy-api-key')
    except Exception as e:
        logger.error(f"Error fetching API key from Secrets Manager {e}")
        raise

def upload_to_s3 (df, s3_path):
    "Upoad DataFrame to S3"
    try:
        if df.empty:
            logger.info(f"No data to upload for {s3_path}")
            return
        
        csv_buffer = StringIO() # Creates an in-memory text buffer that behaves like a file. Saves from saving and working with a local file
        df.to_csv(csv_buffer, index=False)

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_path,
            Body=csv_buffer.getvalue()
        )
        logger.info("Data Uploaded to S3")
    except Exception as e:
        logger.error("Error uploading file into S3")