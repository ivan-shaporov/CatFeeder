import logging
import sys
from datetime import datetime
from os import environ, path

from azure.storage.blob import BlobClient


logging.basicConfig()
logger = logging.getLogger('BlobUpload')
logger.setLevel(logging.INFO)

def upload(filepath, blob_name):
    blob = BlobClient(account_url=environ['BlobUploadUrl'], container_name='catfeedervideo', blob_name=blob_name, credential=environ['BlobUploadSas'])

    for attempt in range(3):
        try:
            logger.info(f'{datetime.now()} {filepath} to {blob_name} attempt #{attempt}')
            with open(filepath, "rb") as data:
                blob.upload_blob(data)
                break
        except Exception as e:
            logger.exception("Upload failed")

filepath = path.splitext(sys.argv[1])[0] # without extension

blob_name = datetime.now().strftime('%Y/%m/%d/%Y%m%d_%H%M')

logger.info(f'{datetime.now()} blob_name={blob_name}')

#blob.upload_blob(sys.stdin.buffer.read())
upload(filepath + '.jpg', blob_name + '.jpg')
upload(filepath + '.mp4', blob_name + '.mp4')
 
logger.info(f'{datetime.now()} {blob_name} finished')
