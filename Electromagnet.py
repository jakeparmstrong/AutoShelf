import time
import RPi.GPIO as GPIO

class Electromagnet:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.relay_pin = pin
        GPIO.setup(self.relay_pin, GPIO.OUT) 
        print("Electromagnet output pin: %s" % (self.relay_pin))
    
    def on(self):
        GPIO.output(self.relay_pin, GPIO.HIGH)
        time.sleep(0.5) #safety

    def off(self):
        GPIO.output(self.relay_pin, GPIO.HIGH)
        time.sleep(0.5) #safety
