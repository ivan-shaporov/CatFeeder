import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='File for upload.')
parser.add_argument('-t', '--time', help='Unix timestamp of the event.', type=lambda s: datetime.fromtimestamp(int(s)))
#parser.add_argument('-t', '--time', type=lambda d: datetime.strptime(d, '%Y%m%d'), help='Time of the event.')
args = parser.parse_args()

filepath = path.splitext(args.file)[0] # without extension

blob_name = args.time.strftime('%Y/%m/%d/%Y%m%d_%H%M')

logger.info(f'{datetime.now()} blob_name={blob_name}')

#blob.upload_blob(sys.stdin.buffer.read())
upload(filepath + '.jpg', blob_name + '.jpg')
upload(filepath + '.mp4', blob_name + '.mp4')
 
logger.info(f'{datetime.now()} {blob_name} finished')
