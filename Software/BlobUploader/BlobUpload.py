from azure.storage.blob import BlobClient
from os import environ
from datetime import datetime
import sys

blob_name = datetime.now().strftime("%Y/%m/%d/%H_%M.h264")

blob = BlobClient(account_url=environ['BlobUploadUrl'], container_name='catfeedervideo', blob_name=blob_name, credential=environ['BlobUploadSas'])

blob.upload_blob(sys.stdin.buffer.read())