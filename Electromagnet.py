import time
import RPi.GPIO as GPIO

class Electromagnet:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.relay_pin = pin
        GPIO.setup(self.relay_pin, GPIO.OUT) 
        GPIO.output(self.relay_pin, GPIO.LOW)
        print("Electromagnet output pin: %s" % (self.relay_pin))

    def on(self):
        print("Electromagnet turned on")
        GPIO.output(self.relay_pin, GPIO.HIGH)
        time.sleep(0.5) #safety

    def off(self):
        print("Electromagnet turned off")
        GPIO.output(self.relay_pin, GPIO.LOW)
#        GPIO.output(self.relay_pin, GPIO.LOW)
        time.sleep(0.5) #safety
