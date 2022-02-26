from DCMotor import DCMotor
from Photoresistor import Photoresistor
from LinearActuator import LinearActuator
import time
import RPi.GPIO as GPIO

DC_MOTOR_ENA = 2
DC_MOTOR_IN1 = 3
DC_MOTOR_IN2 = 4

LIN_ACT_ENA = 14
LIN_ACT_IN3 = 15
LIN_ACT_IN4 = 18

PHOTORES = 17

def dc_class_test():
    print("- DCMotor Class test -")
    dcmotor = DCMotor(DC_MOTOR_ENA, DC_MOTOR_IN1, DC_MOTOR_IN2)
    print("Motor forward")
    dcmotor.fwd()
    time.sleep(5)
    print("Motor backward")
    dcmotor.bwd()
    time.sleep(5)
    dcmotor.brake()
    print("DC Motor Class test finished.")

def la_class_test():
    print("- Linear Actuator Class test -")
    linact = LinearActuator(LIN_ACT_ENA, LIN_ACT_IN3, LIN_ACT_IN4)
    print("LA forward")
    linact.fwd()
    time.sleep(5)
    print("LA backward")
    linact.bwd()
    time.sleep(5)
    linact.brake()
    print("LinearActuator Class test finished.")

def photoresistor_test():
    print("- Photoresistor Class Test -")
    photosensor = Photoresistor(PHOTORES)
    for i in range(20):
        photosensor.print_pin_value()
        time.sleep(0.25)
    print("Photoresistor Class Test finished.")

# dc_class_test() -- pass
# la_class_test() -- pass
photoresistor_test()
GPIO.cleanup()
