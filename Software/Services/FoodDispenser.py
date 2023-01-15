import logging
import sys
from time import sleep
import RPi.GPIO as GPIO
import Light

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
    GPIO.output(PinInput1, GPIO.LOW)
    GPIO.output(PinInput2, GPIO.HIGH)

def _RotateCounterClockwise():
    GPIO.output(PinInput2, GPIO.LOW)
    GPIO.output(PinInput1, GPIO.HIGH)

def StopMotor():
    GPIO.output(PinInput1, GPIO.LOW);
    GPIO.output(PinInput2, GPIO.LOW);

def _Rotate(time, duty_cycle):
    rotate = _RotateCounterClockwise if duty_cycle > 0 else _RotateClockwise
    duty_cycle = abs(duty_cycle)

    step = .05
    on = step * duty_cycle
    off = step * (1 - duty_cycle)

    t = 0
    while t < time:
        if duty_cycle != 0:
            rotate()
            sleep(on)
        if duty_cycle != 1:
            StopMotor()
            sleep(off)
        t += step
    StopMotor()

def Feed(profile):
    _Init()

    try:
        logger.info(f'Feed cycle: {profile}')
        for t, duty_cycle in profile:
            _Rotate(t, duty_cycle)
        return True
    except:
        logger.exception('Feed failed')
        StopMotor()
        return False


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    logger.setLevel(logging.INFO)

    from Config import FoodCycleProfile

    Light.On()
    Feed(FoodCycleProfile)
    Light.Off()
