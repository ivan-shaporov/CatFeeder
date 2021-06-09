import argparse
import logging
import requests

logger = logging.getLogger('CatFeeder')

def AnalyzeImage(blobname, config):

    imageUrl = f'{GetImageUrl(blobname, config)}?{config.ReadSas}'

    logger.info(f'Analyze imageUrl={imageUrl}')

    response = requests.post(
        config.AzureCognitiveServiceUrl, 
        json={'Url': imageUrl}, 
        headers={'Content-Type':'application/json', 'Prediction-Key': config.AzureCognitiveServiceKey})

    if response.status_code != 200:
        logger.error(f'Analyze request failed {response.status_code}: {response.reason}')
        return None

    results = [p for p in response.json()['predictions'] if p['probability'] > config.DetectionThreshold and p['tagName'] not in ['FoodPebble', 'Glare']]

    return results

def GetImageUrl(blobname, config): return f'https://{config.StorageAccount}.blob.core.windows.net/{config.StorageContainer}/{blobname}'

if __name__ == '__main__':
    import Config

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File for analysis.')
    args = parser.parse_args()

    results = AnalyzeImage(args.file, Config)
    print (results)

    tags = [r['tagName'] for r in results]
    emptyPlate = 'EmptyPlate' in tags
    liftedTrunk = 'LiftedTrunk' in tags
    trunk = 'Trunk' in tags
    foodPile = 'FoodPile' in tags

    if emptyPlate: print('emptyPlate')
    if liftedTrunk: print('liftedTrunk')
    if trunk: print('trunk')
    if foodPile: print('foodPile')