import argparse
import logging
from datetime import datetime
import requests

import AnalyzeImageConfig

logging.basicConfig()
logger = logging.getLogger('AnalyzeImage')
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='File for analysis.')
args = parser.parse_args()

def AnalyzeImage(filename, config):

    imageUrl = f'https://{config.StorageAccount}.blob.core.windows.net/{config.StorageContainer}/{filename}?{config.ReadSas}'

    logger.info(f'{datetime.now()} imageUrl={imageUrl}')

    response = requests.post(
        config.AzureCognitiveServiceUrl, 
        json={'Url': imageUrl}, 
        headers={'Content-Type':'application/json', 'Prediction-Key': config.AzureCognitiveServiceKey})

    if response.status_code != 200:
        logger.error(f'{datetime.now()} Analyze request failed {response.status_code}: {response.reason}')
        return None

    results = [p for p in response.json()['predictions'] if p['probability'] > config.DetectionThreshold and p['tagName'] not in ['FoodPebble', 'Glare']]

    return results

results = AnalyzeImage(args.file, AnalyzeImageConfig)

print (results)
