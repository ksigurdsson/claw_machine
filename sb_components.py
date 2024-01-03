from machine import Pin

class pico_motor_driver:
    """SB Components Pico-Motor-Driver HAT

    DC motor driver powered by the L293D H-bridge

    See: https://github.com/sbcshop/Pico-Motor-Driver
    """

    def __init__(self,
                 in1=Pin(21, Pin.OUT),
                 in2=Pin(20, Pin.OUT),
                 in3=Pin(19, Pin.OUT),
                 in4=Pin(18, Pin.OUT),
                 en1=Pin(17, Pin.OUT),
                 en2=Pin(16, Pin.OUT)):

        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.en1 = en1
        self.en2 = en2

    def motor1_forward(self):
        self.en1.off()
        self.in1.on()
        self.in2.off()
        self.en1.on()

    def motor1_reverse(self):
        self.en1.off()
        self.in1.off()
        self.in2.on()
        self.en1.on()

    def motor1_stop(self):
        self.en1.off()

    def motor2_forward(self):
        self.en2.off()
        self.in3.on()
        self.in4.off()
        self.en2.on()

    def motor2_reverse(self):
        self.en2.off()
        self.in3.off()
        self.in4.on()
        self.en2.on()

    def motor2_stop(self):
        self.en2.off()
