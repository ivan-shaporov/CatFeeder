import argparse
from datetime import datetime
import logging
from os import path, rename
from time import sleep

from azure.storage.blob import BlobClient


logger = logging.getLogger('CatFeeder')

def UploadBlob(filepath, blob_name, config):
    blob = _GetBlobClient(blob_name, config)

    for attempt in range(config.UploadRetryCount):
        try:
            logger.info(f'{filepath} to {blob_name} attempt #{attempt}')
            with open(filepath, 'rb') as data:
                blob.upload_blob(data)
                logger.info(f'{blob_name} uploaded')
                return True
        except Exception as e:
            logger.exception("Upload failed")
            sleep(8 ** (attempt + 1))

    archivePath = path.join(path.dirname(path.abspath(__file__)), 'FailedUploads', path.basename(blob_name))
    rename(filepath, archivePath)
    return False

def GetBlobnbame(time): return time.strftime('%Y/%m/%d/%Y%m%d_%H%M')

def UploadPackage(filePath, time, config):
    filename = path.splitext(filePath)[0] # with path, without extension

    blob_name = GetBlobnbame(time)

    logger.info(f'blob_name={blob_name}')

    jpegAvailable = UploadBlob(filename + '.jpg', blob_name + '.jpg', config)
    UploadBlob(filename + '.mp4', blob_name + '.mp4', config)
    
    logger.info(f'{blob_name} finished')

    return jpegAvailable

def UploadMetadata(metadata, blob_name, config):
    blob = _GetBlobClient(blob_name, config)
    blob.set_blob_metadata(metadata)
    logger.info(f'{metadata} uploaded')

def _GetBlobClient(blob_name, config):
    account_url = f'https://{config.StorageAccount}.blob.core.windows.net'

    blob = BlobClient(
        account_url=account_url,
        container_name=config.StorageContainer,
        blob_name=blob_name, 
        credential=config.BlobUploadSas)

    return blob

if __name__ == '__main__':
    import Config

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File for upload.')
    parser.add_argument('-t', '--time', help='Unix timestamp of the event.', type=lambda s: datetime.fromtimestamp(int(s)))
    args = parser.parse_args()

    UploadPackage(args.file, args.time, Config)