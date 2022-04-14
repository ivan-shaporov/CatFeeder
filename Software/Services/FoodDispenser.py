import logging
import sys
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

def TrunkDown(trunkMovementTime):
    _Init()

    _RotateCounterClockwise()
    sleep(trunkMovementTime)
    StopMotor()

def Feed(config):
    _Init()

    try:
        _RotateCounterClockwise()
        sleep(config.TrunkMovementTimeUp)
        StopMotor()

        sleep(config.TrunkLoadTime)

        _RotateClockwise()
        sleep(config.TrunkMovementTimeDown)
        StopMotor()
        return True
    except:
        logger.exception('Feed failed')
        StopMotor()
        return False

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    logger.setLevel(logging.INFO)

    if len(sys.argv) == 2:
        dt = float(sys.argv[1])
        _Init()
        if dt > 0: _RotateClockwise()
        else: _RotateCounterClockwise()
        sleep(abs(dt))
        StopMotor()
    else:
        import Config
        Feed(Config)