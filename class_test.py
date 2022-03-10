from DCMotor import DCMotor
from Photoresistor import Photoresistor
from LinearActuator import LinearActuator
from Electromagnet import Electromagnet
from HallEffectSensor import HallEffectSensor
from EnumTypes import Magnet
import time
import RPi.GPIO as GPIO

DC_MOTOR_ENA = 2
DC_MOTOR_IN1 = 3
DC_MOTOR_IN2 = 4

LIN_ACT_ENA = 14
LIN_ACT_IN3 = 15
LIN_ACT_IN4 = 18
LIN_ACT_SIG = 23

PHOTORES = -17
HE_SENSOR = 17

ELECTROMAG = 22

def dc_class_test():
    print("- DCMotor Class test -")
    dcmotor = DCMotor(DC_MOTOR_ENA, DC_MOTOR_IN1, DC_MOTOR_IN2)
    print("Motor forward")
    dcmotor.fwd()
    #dcmotor.brake()
    time.sleep(35)
    print("Braking")
    dcmotor.brake()
    time.sleep(5)
    print("Motor backward")
    dcmotor.bwd()
    time.sleep(35)
    print("Braking")
    dcmotor.brake()
    time.sleep(5)
    print("DC Motor Class test finished.")
    GPIO.cleanup()

def la_class_test():
    print("- Linear Actuator Class test -")
    linact = LinearActuator(LIN_ACT_ENA, LIN_ACT_IN3, LIN_ACT_IN4, LIN_ACT_SIG)
#    print("LA forward")
#    linact.fwd()
#    time.sleep(5)
#    print("LA backward")
#    linact.bwd()
#    time.sleep(5)
#    linact.brake()
    print("Extending Fully")
    linact.extend_fully()
    print("Retracting Fully")
    linact.retract_fully()
    print("LinearActuator Class test finished.")
    GPIO.cleanup()

def la_encoder_test():
    linact = LinearActuator(LIN_ACT_ENA, LIN_ACT_IN3, LIN_ACT_IN4, LIN_ACT_SIG)
    linact.test_encoder_fwd()
    linact.test_encoder_bwd()
    GPIO.cleanup()
    

def electromagnet_test():
    em = Electromagnet(ELECTROMAG)
    do_again = True
    while do_again == True:
        input("Push enter to turn on electromagnet.")
        print("Electromagnet ON")
        em.on()
        input("Push enter to turn off electromagnet.")
        print("Electromagnet OFF")
        em.off()
        val = input("To run test again, press 'y' and then enter. To end test, push enter only:")
        do_again = True if val == 'y' else False
    print("Electromagnet Class Test finished.")
    GPIO.cleanup()

def hall_effect_sensor_test():
    print("- Hall Effect Sensor Test -")
    hes = HallEffectSensor(HE_SENSOR)
    do_again = True
    while do_again == True:
        for i in range(20):
            if Magnet(hes.get_pin_value()) == Magnet.NEAR:
                print("Magnet is close!")
            time.sleep(0.25)
        val = input("To run test again, press 'y' and then enter. To end test, push enter only:")
        do_again = True if val == 'y' else False
    print("Hall Effect Sensor Class Test finished.")
    GPIO.cleanup()

def photoresistor_test():
    print("- Photoresistor Class Test -")
    photosensor = Photoresistor(PHOTORES)
    for i in range(20):
        photosensor.print_pin_value()
        time.sleep(0.25)
    print("Photoresistor Class Test finished.")
    GPIO.cleanup()

def up_one_floor():
    floor = 1
    hes = HallEffectSensor(HE_SENSOR)
    elevator = DCMotor(DC_MOTOR_ENA, DC_MOTOR_IN1, DC_MOTOR_IN2)
    last_he_reading = Magnet(hes.get_pin_value())  # stores the last hall-effect sensor reading during a floor change
    elevator.fwd()
    print("Going up")
    current_floor = 0
    #spins with motor running, until 
    while current_floor != floor:
      if (Magnet(hes.get_pin_value()) == Magnet.NEAR) and (last_he_reading == Magnet.FAR):
      # got to next floor
        current_floor = (current_floor + 1)
        last_he_reading = Magnet.NEAR
        # TODO remove debug
        print("Just arrived at floor %s" % (current_floor))
      elif (Magnet(hes.get_pin_value()) == Magnet.FAR) and (last_he_reading == Magnet.NEAR):
        # got out of zone of last noted magnet
        last_he_reading = Magnet.FAR
        # TODO remove debug
        print("Just got out of zone of last noted magnet: " + str(current_floor))
    elevator.brake()
    time.sleep(5)
    elevator.bwd()
    while current_floor != 0:
      if (Magnet(hes.get_pin_value()) == Magnet.NEAR) and (last_he_reading == Magnet.FAR):
      # got to next floor
        current_floor = (current_floor - 1)
        last_he_reading = Magnet.NEAR
        # TODO remove debug
        print("Just arrived at floor %s" % (current_floor))
      elif (Magnet(hes.get_pin_value()) == Magnet.FAR) and (last_he_reading == Magnet.NEAR):
        # got out of zone of last noted magnet
        last_he_reading = Magnet.FAR
        # TODO remove debug
        print("Just got out of zone of last noted magnet: " + str(current_floor))
    elevator.brake()
    time.sleep(5)


print("--- Class Unit Test Suite ---")
print("LinearActuator: 'l'")
print("LinearActuator encoder test: 'c")
print("DCMotor: 'd'")
print("Photoresistor: 'p'")
print("Electromagnet: 'e'")
print("HallEffectSensor: 'h'")
whichtest = input("Select test(s) to run: ")
if 'l' in whichtest:
    la_class_test()
if 'd' in whichtest:
    dc_class_test()
if 'p' in whichtest:
    photoresistor_test()
if 'e' in whichtest:
    electromagnet_test()
if 'h' in whichtest:
    hall_effect_sensor_test()
if 'c' in whichtest:
    la_encoder_test()
#TODO run new la_class_test() with full extendor (start with smaller value)
#TODO run hall_effect_sensor_test()
#TODO run electromagnet_test()
# dc_class_test() -- pass
# la_class_test() -- pass on fwd, bwd, brake
# photoresistor_test() -- pass with v divider, but needs shining light on it
GPIO.cleanup()
