from azure.storage.blob import BlobClient
from os import environ, path
from datetime import datetime
import sys


def upload(filepath, blob_name):
    blob = BlobClient(account_url=environ['BlobUploadUrl'], container_name='catfeedervideo', blob_name=blob_name, credential=environ['BlobUploadSas'])
    with open(filepath, "rb") as data:
        blob.upload_blob(data)

filepath = path.splitext(sys.argv[1])[0] # without extension

blob_name = datetime.now().strftime('%Y/%m/%d/%Y%m%d_%H%M')

print(f'{datetime.now()} blob_name={blob_name}')

#blob.upload_blob(sys.stdin.buffer.read())
upload(filepath + '.jpg', blob_name + '.jpg')
upload(filepath + '.mp4', blob_name + '.mp4')
 
print(f'{datetime.now()} {blob_name} finished')