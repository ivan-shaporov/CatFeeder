import argparse
import logging
import RPi.GPIO as GPIO  

logger = logging.getLogger('CatFeeder')


def On(config): 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(config.LightPin, GPIO.OUT)
    GPIO.output(config.LightPin, GPIO.HIGH)
    logger.info(f'Light on')

def Off(config): 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(config.LightPin, GPIO.OUT)
    GPIO.output(config.LightPin, GPIO.LOW)
    logger.info(f'Light off')

if __name__ == '__main__':
    import Config

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-on', action='store_true')
    group.add_argument('-off', action='store_true')
    args = parser.parse_args()

    On(Config) if args.on else Off(Config)