import RPi.GPIO as GPIO
import time

class DCMotor:
    def __init__(self, ena1, in1, in2):
        GPIO.setmode(GPIO.BCM)
        self.DC_MOTOR_ENA = ena1
        self.DC_MOTOR_IN1 = in1
        self.DC_MOTOR_IN2 = in2
        GPIO.setup(self.DC_MOTOR_ENA, GPIO.OUT) 
        GPIO.setup(self.DC_MOTOR_IN1, GPIO.OUT) 
        GPIO.setup(self.DC_MOTOR_IN2, GPIO.OUT)
        print("ENA1 pin: %s" % (self.DC_MOTOR_ENA))
        print("IN1 pin: %s" % (self.DC_MOTOR_IN1))
        print("IN2 pin: %s" % (self.DC_MOTOR_IN2))
    
    def brake(self):
        GPIO.output(self.DC_MOTOR_ENA, GPIO.LOW)
        GPIO.output(self.DC_MOTOR_IN1, GPIO.LOW)
        GPIO.output(self.DC_MOTOR_IN2, GPIO.LOW)

    def fwd(self):
        self.brake()
        time.sleep(0.1)
        GPIO.output(self.DC_MOTOR_ENA, GPIO.HIGH)
        GPIO.output(self.DC_MOTOR_IN1, GPIO.HIGH)
        GPIO.output(self.DC_MOTOR_IN2, GPIO.LOW)

    def bwd(self):
        self.brake()
        time.sleep(0.1)
        GPIO.output(self.DC_MOTOR_ENA, GPIO.HIGH)
        GPIO.output(self.DC_MOTOR_IN2, GPIO.HIGH)
        GPIO.output(self.DC_MOTOR_IN1, GPIO.LOW)
