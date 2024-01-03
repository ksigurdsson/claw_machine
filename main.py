import time

from machine       import Pin, Timer
from sb_components import pico_motor_driver

# Hardware Global Config
grab_button     = Pin(0, Pin.IN, Pin.PULL_UP)
stop_button     = Pin(1, Pin.IN, Pin.PULL_UP)
nudge_up_button = Pin(2, Pin.IN, Pin.PULL_UP)
nudge_dn_button = Pin(3, Pin.IN, Pin.PULL_UP)

relay       = Pin(6, Pin.OUT)
led         = Pin("LED", Pin.OUT)

# Global Harware Instances
motor = pico_motor_driver()

# Global Timers
timmy = Timer()

# Global Variables
timmy_timing = False
grab_sequence_en = False
nudge_up_en = False
nudge_dn_en = False
emergency_stop = False

def stop_button_handler(pin):
    """Stop button IRQ handler

    Stops the whole machine
    """

    # Flag that the emergency stop has happened
    global emergency_stop
    emergency_stop = True

    # Deinitialise (stop) timmy the timer
    timmy.deinit()

    # Clear the timer running flag
    global timmy_timing
    timmy_timing = False

    # Put the machine into a safe state i.e. stopped and not grabbing

    # Stop the motor
    motor.motor1_stop()

    # Release the claw
    global relay
    relay.off()

    # Reset the state variables
    # FIXME: Replace these with a single state variable
    global grab_sequence_en
    grab_sequence_en = False

    global nudge_up_en
    nudge_up_en = False

    global nudge_dn_en
    nudge_dn_en = False

def grab_button_handler(pin):
    """Grab button IRQ handler

    Starts the grab sequence
    """

    global grab_sequence_en
    grab_sequence_en = True

def nudge_up_button_handler(pin):
    """Nudge up button IRQ handler

    Starts the sequence to nudge the grabber up
    """

    global nudge_up_en
    nudge_up_en = True

def nudge_dn_button_handler(pin):
    """Nudge down button IRQ handler

    Starts the sequence to nudge the grabber down
    """

    global nudge_dn_en
    nudge_dn_en = True

def timmy_timer_cb(timer):
    """Callback for Timmy the Timer

    """
    global timmy_timing
    timmy_timing = False

def grab_it():

    global timmy_timing
    global relay

    # Start lowering the claw
    motor.motor1_forward()

    # Configure a timer to lower the claw for the right amount of time
    timmy.init(period=12000, mode=Timer.ONE_SHOT, callback=timmy_timer_cb)
    timmy_timing = True

    # Wait for the claw to lower, crapping out if emergency stop is asserted
    while timmy_timing:
        pass

    if emergency_stop: return None

    # Reached the bottom - stop lowering the claw
    motor.motor1_stop()

    # Dwell for a second
    timmy.init(period=1000, mode=Timer.ONE_SHOT, callback=timmy_timer_cb)
    timmy_timing = True
    while timmy_timing:
        pass

    if emergency_stop: return None

    # Engage the claw
    relay.on()

    # Dwell for a second
    timmy.init(period=1000, mode=Timer.ONE_SHOT, callback=timmy_timer_cb)
    timmy_timing = True
    while timmy_timing:
        pass

    if emergency_stop: return None

    # Raise the claw
    # FIXME: Foreach step in this procdure do we need to check that the
    # emergency stop has not been thrown before we do it and if so return?
    motor.motor1_reverse()

    # Configure a timer to lower the claw for the right amount of time
    timmy.init(period=12000, mode=Timer.ONE_SHOT, callback=timmy_timer_cb)
    timmy_timing = True

    # Wait for the claw to raise, crapping out if emergency stop is asserted
    while timmy_timing:
        pass

    if emergency_stop: return None

    # Reached the top - stop raising the claw
    motor.motor1_stop()

    # Dwell for two seconds
    timmy.init(period=2000, mode=Timer.ONE_SHOT, callback=timmy_timer_cb)
    timmy_timing = True
    while timmy_timing:
        pass

    if emergency_stop: return None

    # Release the claw
    relay.off()

    # The grab sequence has finished so clear the enable flag
    global grab_sequence_en
    grab_sequence_en = False

def nudge(direction):

    global timmy_timing

    if direction == "up":
        # Start raising the claw
        motor.motor1_reverse()
    elif direction == "down":
        # Start lowering the claw
        motor.motor1_forward()
    else:
        return

    # Configure a timer to move the claw (i.e. nudge it) for 1 second
    timmy.init(period=1000, mode=Timer.ONE_SHOT, callback=timmy_timer_cb)
    timmy_timing = True

    # Wait for the claw to move, crapping out if emergency stop is asserted
    while timmy_timing:
        pass

    # Having moved the claw, stop the movement
    motor.motor1_stop()

    global nudge_up_en
    nudge_up_en = False

    global nudge_dn_en
    nudge_dn_en = False

def main():

    # Setup the button IRQs
    grab_button.irq(trigger=Pin.IRQ_FALLING, handler=grab_button_handler)
    stop_button.irq(trigger=Pin.IRQ_FALLING, handler=stop_button_handler)
    nudge_up_button.irq(trigger=Pin.IRQ_FALLING, handler=nudge_up_button_handler)
    nudge_dn_button.irq(trigger=Pin.IRQ_FALLING, handler=nudge_dn_button_handler)

    while True:
        if grab_sequence_en:
            grab_it()

        if nudge_up_en:
            nudge("up")

        if nudge_dn_en:
            nudge("down")

        # If there was an emergency stop, reset that now the grab sequence has returned
        global emergency_stop
        emergency_stop = False


if __name__ == "__main__":
    main()
