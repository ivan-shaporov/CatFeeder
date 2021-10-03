import logging
from time import sleep
import RPi.GPIO as GPIO  

logger = logging.getLogger('CatFeeder')

PinInput1 = 7
PinInput2 = 5
ActionTime = 1.0

def _Init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(PinInput1, GPIO.OUT)
    GPIO.setup(PinInput2, GPIO.OUT)
    logger.info(f'FoodDispenser Initialized')

def _RotateClockwise():
    logger.info(f'Rotating clockwise')
    GPIO.output(PinInput1, GPIO.LOW)
    GPIO.output(PinInput2, GPIO.HIGH)

def _RotateCounterClockwise():
    logger.info(f'Rotating counterclockwise')
    GPIO.output(PinInput2, GPIO.LOW)
    GPIO.output(PinInput1, GPIO.HIGH)

def StopMotor():
    logger.info(f'Motor stopping')
    GPIO.output(PinInput1, GPIO.LOW);
    GPIO.output(PinInput2, GPIO.LOW);

def Feed():
    _Init()

    _RotateClockwise()
    sleep(ActionTime)
    StopMotor()

    sleep(1.0);

    _RotateCounterClockwise()
    sleep(ActionTime)
    StopMotor()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    logger.setLevel(logging.INFO)

    Feed()