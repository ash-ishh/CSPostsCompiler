import boto3
import os
import json

from dotenv import load_dotenv
load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
CHECKPOINT_FILE_NAME = os.getenv("CHECKPOINT_FILE_NAME")

if not S3_BUCKET_NAME:
    print("Populate .env with S3_BUCKET_NAME")
    exit(0)

if not CHECKPOINT_FILE_NAME:
    print("Populate .env with CHECKPOINT_FILE_NAME")
    exit(0)

def get_checkpoint():
    s3_client = boto3.client("s3")
    checkpoint = s3_client.get_object(
        Bucket=S3_BUCKET_NAME,
        Key=CHECKPOINT_FILE_NAME
    )
    checkpoint_object = json.loads(checkpoint['Body'].read())
    return checkpoint_object

def set_checkpoint(checkpoint_object):
    s3_client = boto3.client("s3")
    s3_client.put_object(
        Body=json.dumps(checkpoint_object),
        Bucket=S3_BUCKET_NAME,
        Key=CHECKPOINT_FILE_NAME
    )