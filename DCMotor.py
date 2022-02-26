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
    
    def brake(self):
        GPIO.output(DCMotor.DC_MOTOR_ENA, GPIO.LOW)
        GPIO.output(DCMotor.DC_MOTOR_IN1, GPIO.LOW)
        GPIO.output(DCMotor.DC_MOTOR_IN2, GPIO.LOW)

    def fwd(self):
        DCMotor.brake()
        time.sleep(0.1)
        GPIO.output(DCMotor.DC_MOTOR_ENA, GPIO.HIGH)
        GPIO.output(DCMotor.DC_MOTOR_IN1, GPIO.HIGH)
        GPIO.output(DCMotor.DC_MOTOR_IN2, GPIO.LOW)

    def bwd(self):
        DCMotor.brake()
        time.sleep(0.1)
        GPIO.output(DCMotor.DC_MOTOR_ENA, GPIO.HIGH)
        GPIO.output(DCMotor.DC_MOTOR_IN2, GPIO.HIGH)
        GPIO.output(DCMotor.DC_MOTOR_IN1, GPIO.LOW)
