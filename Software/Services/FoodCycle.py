import argparse
from datetime import datetime
import json
import logging
import time
from opencensus.ext.azure.log_exporter import AzureLogHandler, AzureEventHandler
from opencensus.trace import tracer as tracer_module
from opencensus.ext.azure.trace_exporter import AzureExporter

import Light
from AnalyzeImage import AnalyzeImage, GetImageUrl
from BlobUpload import UploadPackage, GetBlobnbame, UploadMetadata
from Camera import StartRecording, StartEncoding, StartExtracting, GetVideoName
from FoodDispenser import Feed, StopMotor

logger = logging.getLogger('CatFeeder')
events = logging.getLogger('CatFeeder_events')


def create_event_properties(trace_id, event_value, **extra_dimensions):
    """Create properties dictionary for event logging with common values"""
    properties = {
        'custom_dimensions': {
            'eventType': 'Food',
            'traceId': trace_id,
            'eventValue': event_value
        }
    }
    # Add any extra dimensions
    properties['custom_dimensions'].update(extra_dimensions)
    return properties


def FullCycle(config, scoops):
    '''
    Returns True if retry is needed.
    '''
    tracer = tracer_module.Tracer(
        exporter=AzureExporter(connection_string=config.AppInsightsConnectionString))

    with tracer.span(name="food_cycle") as span:
        span_context = span.context_tracer.span_context
        try:
            now = localnow()

            profile = config.FoodCycleProfile

            cycleDuration = sum((abs(p[0]) for p in profile))

            p = StartRecording(config, cycleDuration * scoops + config.VideoDuration)

            Light.On()
            events.info(f'Food cycle started. Food {scoops} scoops to be fed.',
                        extra=create_event_properties(span_context.trace_id, 'started'))

            logger.info(f'giving {scoops} scoops...')
            for _ in range(scoops):
                if not Feed(profile):
                    break

            error = p.wait()
            if error != 0:
                logger.error('Video recording failed')
                return False

            p = StartEncoding(config)

            time.sleep(config.LightDuration)
            Light.Off()

            events.info('Food cycle encoding.', extra=create_event_properties(span_context.trace_id, 'encoding'))

            if p.wait() != 0:
                logger.error('Video encoding failed')
                return False

            events.info('Food cycle extracting image.',
                        extra=create_event_properties(span_context.trace_id, 'extracting_image'))

            if StartExtracting(config, cycleDuration * scoops + config.FoodPourDelay).wait() != 0:
                logger.error('Poster extracting failed')
                return False

            events.info('Food cycle analyzing.', extra=create_event_properties(span_context.trace_id, 'analyzing'))

            jpegAvailable = UploadPackage(GetVideoName(config), now, config)

            if not jpegAvailable:
                return False

            blobname = GetBlobnbame(now) + '.jpg'

            results = AnalyzeImage(blobname, config)

            print(results)

            tags = {r['tagName']: r['probability'] for r in results}
            emptyPlate = 'EmptyPlate' in tags
            foodPile = 'FoodPile' in tags

            imageUrl = GetImageUrl(blobname, config)

            noFood = (not foodPile) and emptyPlate

            eventValue = 'skipped' if scoops <= 0 else 'failed' if noFood else 'delivered'

            properties = create_event_properties(
                span_context.trace_id, eventValue, imageUrl=imageUrl, tags=json.dumps(tags))

            if noFood:
                logger.warning('Food cycle completed. No food.', extra=properties)
            else:
                logger.info('Food cycle completed.', extra=properties)

            events.info(f'Food cycle completed. Food {eventValue}.', extra=properties)

            UploadMetadata({'imagedetections': json.dumps(results)}, blobname, config)

            return noFood and scoops > 0
        except Exception:
            logger.exception('Full cycle failed')
            StopMotor()
            Light.Off()
            try:
                events.info('Food cycle exception.', extra=create_event_properties(span_context.trace_id, 'exception'))
            except Exception:
                pass
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
        logger.info('Retrying full cycle...')
        FullCycle(Config, scoops=args.scoops)
