import RPi.GPIO as GPIO
import time

class LinearActuator:
    def __init__(self, ena2, in3, in4, sig):
        self.LIN_ACT_ENA = ena2
        self.LIN_ACT_IN3 = in3
        self.LIN_ACT_IN4 = in4
        self.LIN_ACT_SIG = sig
        self.PULSE_PER_INCH = 11278 #number of encoder pulses per inch for this model
        self.timeout = 5 # timeout for full extends/retracts in seconds

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LIN_ACT_ENA, GPIO.OUT) 
        GPIO.setup(self.LIN_ACT_IN3, GPIO.OUT) 
        GPIO.setup(self.LIN_ACT_IN4, GPIO.OUT)
        GPIO.setup(self.LIN_ACT_SIG, GPIO.IN)

        print("ENA2 pin: %s" % (self.LIN_ACT_ENA))
        print("IN3 pin: %s" % (self.LIN_ACT_IN3))
        print("IN4 pin: %s" % (self.LIN_ACT_IN4))
        print("SIGNAL pin: %s" % (self.LIN_ACT_SIG))

    
    def brake(self):
        GPIO.output(self.LIN_ACT_ENA, GPIO.LOW)
        GPIO.output(self.LIN_ACT_IN3, GPIO.LOW)
        GPIO.output(self.LIN_ACT_IN4, GPIO.LOW)

    def fwd(self):
        self.brake()
        time.sleep(0.1)
        GPIO.output(self.LIN_ACT_ENA, GPIO.HIGH)
        GPIO.output(self.LIN_ACT_IN3, GPIO.HIGH)
        GPIO.output(self.LIN_ACT_IN4, GPIO.LOW)
        
    def bwd(self):
        self.brake()
        time.sleep(0.1)
        GPIO.output(self.LIN_ACT_ENA, GPIO.HIGH)
        GPIO.output(self.LIN_ACT_IN4, GPIO.HIGH)
        GPIO.output(self.LIN_ACT_IN3, GPIO.LOW)

    def extend_fully(self):
        encoder_count = 0
        last_encoder_sig = GPIO.input(self.LIN_ACT_SIG)
        start_time = time.perf_counter()
        self.fwd()
        # test using fewer inches
        full_length = self.PULSE_PER_INCH * 12
        while encoder_count < full_length:
            if last_encoder_sig != GPIO.input(self.LIN_ACT_SIG):
                encoder_count += 1
                last_encoder_sig = (last_encoder_sig + 1) % 2
            if (time.perf_counter() - start_time) > self.timeout:
                print("Timeout on full-extend.")
                break
        self.brake()
    
    def retract_fully(self):
        encoder_count = 0
        last_encoder_sig = GPIO.input(self.LIN_ACT_SIG)
        self.bwd()
        start_time = time.perf_counter()
        # test using fewer inches
        full_length = self.PULSE_PER_INCH * 12
        while encoder_count < full_length:
            if last_encoder_sig != GPIO.input(self.LIN_ACT_SIG):
                encoder_count += 1
                last_encoder_sig = (last_encoder_sig + 1) % 2
            if (time.perf_counter() - start_time) > self.timeout:
                print("Timeout on full-retract.")
                break
        self.brake()