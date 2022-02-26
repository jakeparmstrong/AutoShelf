import RPi.GPIO as GPIO

class DigitalSensor:
    def __init__(self, input_pin_num):
        GPIO.setmode(GPIO.BCM)
        self.input_pin = input_pin_num
        GPIO.setup(self.input, GPIO.IN) 

    def get_pin_value(self):
        return GPIO.input(self.input_pin)

    def print_pin_value(self):
        pin_reading = self.get_pin_value()
        print(pin_reading)