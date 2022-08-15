import argparse
from datetime import datetime
import json
import logging
import time
from opencensus.ext.azure.log_exporter import AzureLogHandler, AzureEventHandler

import Light
from AnalyzeImage import AnalyzeImage, GetImageUrl
from BlobUpload import UploadPackage, GetBlobnbame, UploadMetadata
from Camera import StartRecording, StartEncoding, StartExtracting, GetVideoName
from FoodDispenser import Feed, StopMotor

logger = logging.getLogger('CatFeeder')
events = logging.getLogger('CatFeeder_events')

def FullCycle(config, scoops):
    '''
    Returns True if retry is needed.
    '''

    try:
        now = localnow()

        cycleDuration = config.TrunkMovementTimeUp + config.TrunkLoadTime + config.TrunkMovementTimeDown

        p = StartRecording(config, cycleDuration * scoops + config.VideoDuration)

        Light.On()

        logger.info(f'giving {scoops} scoops...')
        for _ in range(scoops):
            if not Feed(config): break
        
        error = p.wait()
        if error != 0:
            logger.error(f'Video recording failed')
            return False

        p = StartEncoding(config)

        time.sleep(config.LightDuration)
        Light.Off()

        if p.wait() != 0:
            logger.error(f'Video encoding failed')
            return False

        if StartExtracting(config, cycleDuration * scoops + 4.5).wait() != 0:
            logger.error(f'Poster extracting failed')
            return False

        jpegAvailable = UploadPackage(GetVideoName(config), now, config)

        if not jpegAvailable:
            return False

        blobname = GetBlobnbame(now) + '.jpg'

        results = AnalyzeImage(blobname, config)

        print (results)

        tags = {r['tagName']: r['probability'] for r in results}
        emptyPlate = 'EmptyPlate' in tags
        foodPile = 'FoodPile' in tags

        imageUrl = GetImageUrl(blobname, config)
        properties = {'custom_dimensions': {'imageUrl': imageUrl, 'tags': json.dumps(tags)}}

        noFood = (not foodPile) and emptyPlate

        if noFood:
            logger.warning(f'Food cycle completed. No food.', extra=properties)
        else:
            logger.info(f'Food cycle completed.', extra=properties)

        eventValue = 'skipped' if scoops <= 0 else 'failed' if noFood else 'delivered'
        properties['custom_dimensions']['eventType'] = 'Food'
        properties['custom_dimensions']['eventValue'] = eventValue
        properties['custom_dimensions']['eventTime'] = str(now)
        events.info(f'Food cycle completed. Food {eventValue}.', extra=properties)

        UploadMetadata({'imagedetections': json.dumps(results)}, blobname, config)

        return noFood and scoops > 0
    except:
        logger.exception('Full cycle failed')
        StopMotor()
        Light.Off()
        return False

def localnow(): return datetime.now(datetime.utcnow().astimezone().tzinfo)

if __name__ == '__main__':
    import Config

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
    logger.addHandler(AzureLogHandler(connection_string=Config.AppInsightsConnectionString))
    events.addHandler(AzureEventHandler(connection_string=Config.AppInsightsConnectionString))

    logger.setLevel(logging.INFO)
    events.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-scoops', '-s', type=int, default=1)
    parser.add_argument('-videoDuration', '-v', type=int, default=Config.VideoDuration)
    args = parser.parse_args()

    if args.videoDuration != Config.VideoDuration:
        Config.VideoDuration = args.videoDuration
        logger.info(f'VideoDuration={Config.VideoDuration}')

    retry = FullCycle(Config, scoops=args.scoops)

    if retry:
        logger.info(f'Retrying full cycle...')
        FullCycle(Config, scoops=args.scoops)
