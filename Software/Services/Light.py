import argparse
import logging
import RPi.GPIO as GPIO  

logger = logging.getLogger('CatFeeder')

LightPin = 8

def On(): 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(LightPin, GPIO.OUT)
    GPIO.output(LightPin, GPIO.HIGH)
    logger.info(f'Light on')

def Off(): 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(LightPin, GPIO.OUT)
    GPIO.output(LightPin, GPIO.LOW)
    logger.info(f'Light off')

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-on', action='store_true')
    group.add_argument('-off', action='store_true')
    args = parser.parse_args()

    On() if args.on else Off()