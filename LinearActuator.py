import RPi.GPIO as GPIO
import time

class LinearActuator:
    def __init__(self, ena2, in3, in4, sig):
        self.LIN_ACT_ENA = ena2
        self.LIN_ACT_IN3 = in3
        self.LIN_ACT_IN4 = in4
        self.LIN_ACT_SIG = sig
        self.PULSE_PER_INCH = 5946 #number of encoder pulses per inch for this model
        self.MOTOR_DRIVER_PWM_FREQUENCY = 1000
        self.MOTOR_DRIVER_PWM_DUTY_CYCLE = 90
        self.timeout = 4 # timeout for full extends/retracts in seconds
        self.EXTENSION_TIME = 60 # 60 seconds for time-based extension/retraction
        self.USE_ENCODERS = False # Whether to use encoders when extending/retracting vs hard-coded timer

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LIN_ACT_ENA, GPIO.OUT) 
        GPIO.setup(self.LIN_ACT_IN3, GPIO.OUT) 
        GPIO.setup(self.LIN_ACT_IN4, GPIO.OUT)
        GPIO.setup(self.LIN_ACT_SIG, GPIO.IN)

        self.IN3_PWM = GPIO.PWM(self.LIN_ACT_IN3, 10000)
        self.IN4_PWM = GPIO.PWM(self.LIN_ACT_IN4, 10000)

        print("ENA2 pin: %s" % (self.LIN_ACT_ENA))
        print("IN3 pin: %s" % (self.LIN_ACT_IN3))
        print("IN4 pin: %s" % (self.LIN_ACT_IN4))
        print("SIGNAL pin: %s" % (self.LIN_ACT_SIG))

    def brake(self):
        GPIO.output(self.LIN_ACT_ENA, GPIO.LOW)
        self.IN3_PWM.stop()
        self.IN4_PWM.stop()

    def fwd(self):
        self.brake()
        time.sleep(0.1)
        #self.ENA_PWM.start(self.MOTOR_DRIVER_PWM_DUTY_CYCLE)
        GPIO.output(self.LIN_ACT_ENA, GPIO.HIGH)
        self.IN3_PWM.start(self.MOTOR_DRIVER_PWM_DUTY_CYCLE)
        self.IN4_PWM.stop()
        #GPIO.output(self.LIN_ACT_IN3, GPIO.HIGH)
        #GPIO.output(self.LIN_ACT_IN4, GPIO.LOW)
        
    def bwd(self):
        self.brake()
        time.sleep(0.1)
        #self.ENA_PWM.start(self.MOTOR_DRIVER_PWM_DUTY_CYCLE)
        #GPIO.output(self.LIN_ACT_IN4, GPIO.HIGH)
        #GPIO.output(self.LIN_ACT_IN3, GPIO.LOW)
        
        GPIO.output(self.LIN_ACT_ENA, GPIO.HIGH)
        self.IN4_PWM.start(self.MOTOR_DRIVER_PWM_DUTY_CYCLE)
        self.IN3_PWM.stop()

    def extend_fully_by_encoder(self):
        encoder_count = 0
        last_encoder_sig = GPIO.input(self.LIN_ACT_SIG)
        print("encoder input = %s" % (GPIO.input(self.LIN_ACT_SIG)))
        start_time = time.perf_counter()
        full_length = self.PULSE_PER_INCH * 12
        self.fwd()
        while encoder_count < full_length:
            if last_encoder_sig != GPIO.input(self.LIN_ACT_SIG):
                encoder_count += 1
                last_encoder_sig = (last_encoder_sig + 1) % 2
            if (time.perf_counter() - start_time) > self.timeout:
                print("Timeout on full-extend.")
                print(encoder_count)
                break

    def extend_fully_by_time(self):
        start_time = time.perf_counter()
        self.fwd()
        while (time.perf_counter() - start_time) < self.EXTENSION_TIME:
            continue

    def extend_fully(self):
        if self.USE_ENCODERS:
            extend_fully_by_encoder(self)
        else:
            extend_fully_by_time(self)
        self.brake()

    def test_encoder_fwd(self):
        print("Testing encoder on linear actuator (forward)")
        encoder_count = 0
        last_encoder_sig = GPIO.input(self.LIN_ACT_SIG)
        full_length = self.PULSE_PER_INCH * 12
        self.fwd()
        # test using fewer inches
        while encoder_count < full_length:
            if last_encoder_sig != GPIO.input(self.LIN_ACT_SIG):
                encoder_count += 1
                last_encoder_sig = (last_encoder_sig + 1) % 2 # 1 -> 0; 0->1 [not reading again in case it changed?]
            print(last_encoder_sig)
            #print(encoder_count)
        self.brake()

    def test_encoder_bwd(self):
        print("Testing encoder on linear actuator (backward)")
        encoder_count = 0
        last_encoder_sig = GPIO.input(self.LIN_ACT_SIG)
        full_length = self.PULSE_PER_INCH * 12
        self.bwd()
        # test using fewer inches
        while encoder_count < full_length:
            if last_encoder_sig != GPIO.input(self.LIN_ACT_SIG):
                encoder_count += 1
                last_encoder_sig = (last_encoder_sig + 1) % 2 # 1 -> 0; 0->1 [not reading again in case it changed?]
                #update the last time the encoder moved
                last_t = time.perf_counter()
            if (time.perf_counter() - last_t) > self.timeout:
                # it has been more than [self.timeout] seconds since the encoder changed => we are retracted
                break
            # failsafe timeout
            if (time.perf_counter() - start_time) > self.timeout:
                print("Timeout on full-retract.")
                break
            print(last_encoder_sig)
            #print(encoder_count)
        self.brake()

    def retract_fully_by_encoder(self):
        encoder_count = 0
        print("encoder input = %s" % (GPIO.input(self.LIN_ACT_SIG)))
        last_encoder_sig = GPIO.input(self.LIN_ACT_SIG)
        self.bwd()
        # test using fewer inches
        full_length = self.PULSE_PER_INCH * 12
        start_time = time.perf_counter()
        last_t = start_time
        while encoder_count < full_length:
            print("encoder ct = %s" % (encoder_count))
            if last_encoder_sig != GPIO.input(self.LIN_ACT_SIG):
                encoder_count += 1
                last_encoder_sig = (last_encoder_sig + 1) % 2
                #update the last time the encoder moved
                last_t = time.perf_counter()
            if (time.perf_counter() - last_t) > self.timeout:
                # it has been more than [self.timeout] seconds since the encoder changed => we are retracted
                break
            # failsafe timeout
            if (time.perf_counter() - start_time) > self.timeout:
                print("Timeout on full-retract.")
                print(encoder_count)
                break

    def retract_fully_by_time(self):
        start_time = time.perf_counter()
        self.bwd()
        while (time.perf_counter() - start_time) < self.EXTENSION_TIME:
            continue

    def retract_fully(self):
        if self.USE_ENCODERS:
            retract_fully_by_encoder(self)
        else:
            retract_fully_by_time(self)
        self.brake()
