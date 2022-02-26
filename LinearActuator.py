import RPi.GPIO as GPIO
import time

class LinearActuator:
    def __init__(self, ena2, in3, in4):
        GPIO.setmode(GPIO.BCM)
        self.LIN_ACT_ENA = ena2
        self.LIN_ACT_IN3 = in3
        self.LIN_ACT_IN4 = in4
        GPIO.setup(self.LIN_ACT_ENA, GPIO.OUT) 
        GPIO.setup(self.LIN_ACT_IN3, GPIO.OUT) 
        GPIO.setup(self.LIN_ACT_IN4, GPIO.OUT)
    
    def brake(self):
        GPIO.output(LinearActuator.LIN_ACT_ENA, GPIO.LOW)
        GPIO.output(LinearActuator.LIN_ACT_IN3, GPIO.LOW)
        GPIO.output(LinearActuator.LIN_ACT_IN4, GPIO.LOW)

    def fwd(self):
        self.brake()
        time.sleep(0.1)
        GPIO.output(LinearActuator.LIN_ACT_ENA, GPIO.HIGH)
        GPIO.output(LinearActuator.LIN_ACT_IN3, GPIO.HIGH)
        GPIO.output(LinearActuator.LIN_ACT_IN4, GPIO.LOW)
        
    def bwd(self):
        self.brake()
        time.sleep(0.1)
        GPIO.output(LinearActuator.LIN_ACT_ENA, GPIO.HIGH)
        GPIO.output(LinearActuator.LIN_ACT_IN4, GPIO.HIGH)
        GPIO.output(LinearActuator.LIN_ACT_IN3, GPIO.LOW)