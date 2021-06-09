from datetime import datetime
import json
import logging
import time
from opencensus.ext.azure.log_exporter import AzureLogHandler

import Light
from AnalyzeImage import AnalyzeImage, GetImageUrl
from BlobUpload import UploadPackage, GetBlobnbame
from Camera import StartRecording, StartEncoding, StartExtracting, GetVideoName
from FoodDispenser import Feed

logger = logging.getLogger('CatFeeder')

def FullCycle(config):

    try:
        p = StartRecording(config)

        Light.On()

        Feed()
        
        error = p.wait()
        if error != 0:
            logger.error(f'Video recording failed')
            return

        p = StartEncoding(Config)

        time.sleep(config.LightDuration)
        Light.Off()

        if p.wait() != 0:
            logger.error(f'Video encoding failed')
            return

        if StartExtracting(Config).wait() != 0:
            logger.error(f'Poster extracting failed')
            return

        jpegAvailable = UploadPackage(GetVideoName(config), now, config)

        if jpegAvailable:
            blobname = GetBlobnbame(now) + '.jpg'

            results = AnalyzeImage(blobname, config)

            print (results)

            tags = {r['tagName']: r['probability'] for r in results}
            emptyPlate = 'EmptyPlate' in tags
            liftedTrunk = 'LiftedTrunk' in tags
            trunk = 'Trunk' in tags
            foodPile = 'FoodPile' in tags

            # if emptyPlate: print('emptyPlate')
            # if liftedTrunk: print('liftedTrunk')
            # if trunk: print('trunk')
            # if foodPile: print('foodPile')

            imageUrl = GetImageUrl(blobname, config)
            properties = {'custom_dimensions': {'imageUrl': imageUrl, 'tags': json.dumps(tags)}}

            if (not foodPile) and (liftedTrunk or trunk or emptyPlate):
                logger.warning(f'Food cycle completed. No food.', extra=properties)
            else:
                logger.info(f'Food cycle completed.', extra=properties)
    except:
        logger.exception()
        Light.Off()

if __name__ == '__main__':
    now = datetime.now()
    import Config

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
    logger.addHandler(AzureLogHandler(connection_string=Config.AppInsightsConnectionString))

    logger.setLevel(logging.INFO)

    FullCycle(Config)
