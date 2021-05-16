from azure.storage.blob import BlobClient
from os import environ
from datetime import datetime
import sys

blob_name = datetime.now().strftime("%Y/%m/%d/%Y%m%d_%H%M.mp4")

print(f'{datetime.now()} blob_name={blob_name}')

blob = BlobClient(account_url=environ['BlobUploadUrl'], container_name='catfeedervideo', blob_name=blob_name, credential=environ['BlobUploadSas'])

blob.upload_blob(sys.stdin.buffer.read())

print(f'{datetime.now()} {blob_name} finished')