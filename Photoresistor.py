import RPi.GPIO as GPIO
from DigitalSensor import DigitalSensor

class Photoresistor(DigitalSensor):
    def __init__(self, input_pin_num):
        super().__init__(input_pin_num)
    