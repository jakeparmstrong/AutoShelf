import RPi.GPIO as GPIO
import time

# pin constants -- RPI 3B+
ELECTROMAG = 23 # Pin number for electromagnet relay pin

DC_MOTOR_ENA = 2
DC_MOTOR_IN1 = 3
DC_MOTOR_IN2 = 4

LIN_ACT_ENA = 14
LIN_ACT_IN3 = 15
LIN_ACT_IN4 = 18

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ELECTROMAG, GPIO.OUT) 

    GPIO.setup(DC_MOTOR_ENA, GPIO.OUT) 
    GPIO.setup(DC_MOTOR_IN1, GPIO.OUT) 
    GPIO.setup(DC_MOTOR_IN2, GPIO.OUT) 

    GPIO.setup(LIN_ACT_ENA, GPIO.OUT) 
    GPIO.setup(LIN_ACT_IN3, GPIO.OUT) 
    GPIO.setup(LIN_ACT_IN4, GPIO.OUT) 

def electromagnet_on():
    GPIO.output(ELECTROMAG, GPIO.HIGH)

def electromagnet_off():
    GPIO.output(ELECTROMAG, GPIO.LOW)

# IN1 - 1 
# IN2 - 0 
# ENA - 1
def dc_motor_fwd():
    dc_motor_off()
    time.sleep(0.1)
    GPIO.output(DC_MOTOR_ENA, GPIO.HIGH)
    GPIO.output(DC_MOTOR_IN1, GPIO.HIGH)
    GPIO.output(DC_MOTOR_IN2, GPIO.LOW)

# IN1 - 0 
# IN2 - 1
# ENA - 1
def dc_motor_bwd():
    dc_motor_off()
    time.sleep(0.1)
    GPIO.output(DC_MOTOR_ENA, GPIO.HIGH)
    GPIO.output(DC_MOTOR_IN2, GPIO.HIGH)
    GPIO.output(DC_MOTOR_IN1, GPIO.LOW)

# IN1 - 0 
# IN2 - 0 
# ENA - 0
def dc_motor_off():
    GPIO.output(DC_MOTOR_ENA, GPIO.LOW)
    GPIO.output(DC_MOTOR_IN1, GPIO.LOW)
    GPIO.output(DC_MOTOR_IN2, GPIO.LOW)

def lin_act_fwd():
    lin_act_off()
    time.sleep(0.1)
    GPIO.output(LIN_ACT_ENA, GPIO.LOW)
    GPIO.output(LIN_ACT_IN3, GPIO.HIGH)
    GPIO.output(LIN_ACT_IN4, GPIO.LOW)

def lin_act_bwd():
    lin_act_off()
    time.sleep(0.1)
    GPIO.output(LIN_ACT_ENA, GPIO.LOW)
    GPIO.output(LIN_ACT_IN4, GPIO.HIGH)
    GPIO.output(LIN_ACT_IN3, GPIO.LOW)

def lin_act_off():
    GPIO.output(LIN_ACT_ENA, GPIO.LOW)
    GPIO.output(LIN_ACT_IN3, GPIO.LOW)
    GPIO.output(LIN_ACT_IN4, GPIO.LOW)

def dc_motor_test():
    print("Motor forward")
    dc_motor_fwd()
    time.sleep(3)
    print("Motor backward")
    dc_motor_bwd()
    time.sleep(3)
    dc_motor_off()
    print("Finished DC Motor test")

def lin_act_test():
    print("Linear actuator forward")
    lin_act_fwd()
    time.sleep(3)
    print("Linear actuator backward")
    lin_act_bwd()
    time.sleep(3)
    lin_act_off()
    print("Finished Linear actuator test")


def em_test():
    print("Turning on electromagnet")
    electromagnet_on()
    time.sleep(3)
    print("Turning off electromagnet")
    electromagnet_off()
    print("Finished electromagnet relay test")

init()
dc_motor_test()
#lin_act_test()
#em_test()
GPIO.cleanup()
