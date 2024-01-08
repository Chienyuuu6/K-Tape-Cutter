import RPi.GPIO as GPIO

# Define GPIO pins for the rotary encoder
CLK = 22  # Rotary encoder CLK pin
DT = 27  # Rotary encoder DT pin
SW = 17   # Rotary encoder SW (push button) pin

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize variables
counter = 0
clk_last_state = GPIO.input(CLK)
dt_last_state = GPIO.input(DT)

# Callback function for the rotary encoder
def rotary_encoder_callback(channel):
    global counter, clk_last_state, dt_last_state

    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)

    if clk_state != clk_last_state:
        if dt_state != clk_state:
            counter += 1
        else:
            counter -= 1

    clk_last_state = clk_state
    dt_last_state = dt_state
