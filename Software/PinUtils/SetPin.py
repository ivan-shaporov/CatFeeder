import sys
import RPi.GPIO as GPIO  


arg = int(sys.argv[1])
pin = abs(arg)

print (pin, arg > 0)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH if arg > 0 else GPIO.LOW)
