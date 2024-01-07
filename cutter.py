import RPi.GPIO as GPIO
import time
from threading import Thread
import encoder

# GPIO setting
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def laser(status):

    laser_pin = 12
    GPIO.setup(laser_pin, GPIO.OUT)
    GPIO.output(laser_pin, status)

laser(GPIO.LOW)


# seq for moving
seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]


# global counter: shared from encoder
# roller motor
# Define the GPIO pins for the stepper motor

if GPIO.event_detected(encoder.CLK):
    print(f"Event detection already enabled for GPIO channel {encoder.CLK}")
else:
    GPIO.add_event_detect(encoder.CLK, GPIO.BOTH, callback=encoder.rotary_encoder_callback)


def roller():
    
    encoder.counter=0

    r_pins =[6,13,19,26]

    for i in r_pins:        
        GPIO.setup(i, GPIO.OUT)
    
    while True:
        print(encoder.counter)
        for i in range(8):
            for y in range(4):
                GPIO.output(r_pins[y], seq[i][y])
            time.sleep(0.001)

        # 14 counts for a square
        if(encoder.counter)==14:
                break
        

# setup motors
# x-axis motor
def motor_x(steps, speed, direction):
    # Define the GPIO pins for the stepper motor    
    x_pins = [18,23,24,25]

    for i in x_pins:        
        GPIO.setup(i, GPIO.OUT)
    
    move_single(x_pins, steps, speed, direction)
    
    
# y-axis motor   
def motor_y(steps, speed, direction):
    # Define the GPIO pins for the stepper motor    
    y_pins = [5,16,20,21]

    for i in y_pins:        
        GPIO.setup(i, GPIO.OUT)
    
    move_single(y_pins, steps, speed, direction)
    
  

# move one motor   
def move_single(pins, steps, speed, direction):
    
    if direction == 0:
        for _ in range(steps):
            print(_)
            for i in range(8):
                for y in range(4):
                    GPIO.output(pins[y], seq[i][y])
                time.sleep(speed)
    else:
        for _ in range(steps):
            print(_)
            for i in range(8):
                for y in range(4):
                    pin=abs(y-(3))
                    GPIO.output(pins[pin], seq[i][y])
                time.sleep(speed)
   

# move a slope
def move_both( speed, direction_x, direction_y):
    thread_x = Thread(target=motor_x, args=(slope, speed, direction_x))
    thread_y = Thread(target=motor_y, args=(slope, speed, direction_y))

    thread_x.start()
    thread_y.start()

    thread_x.join()
    thread_y.join()
    
    
    
# tape cutting format
# move steps
# 5cm
grid = 732 
slope = 42
remain1 = 690
remain4 = 648
remain2 = 282
remain3 = 99

# speed
laser_speed = 0.025
move_speed = 0.001
# onclose
def onclose_u():
    laser(GPIO.LOW)
    motor_y(remain1, move_speed, 0)
    laser(GPIO.HIGH)
    move_both(laser_speed, 0,0)
    laser(GPIO.LOW)
    motor_x(remain1, move_speed, 0)
    laser(GPIO.HIGH)
    move_both(laser_speed, 0,1)
    laser(GPIO.LOW)
    motor_y(remain1, move_speed, 1)
    motor_x(grid, move_speed, 1)   

def onclose_y():
    laser(GPIO.LOW)
    motor_y(remain1, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)
    motor_x(remain2, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    motor_y(remain1, laser_speed,1)
    laser(GPIO.LOW)
    motor_y(remain1, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)
    motor_x(remain2, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_y(remain1, move_speed,1)
    motor_x(grid, move_speed,1)
  
# enclose
def enclose_u():
    motor_y(slope, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_x(remain4, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)
    motor_y(slope, move_speed,1)
    laser(GPIO.HIGH)
    motor_x(grid, move_speed,1)
    laser(GPIO.LOW)
    
    
def enclose_y():
    motor_y(slope, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_x(remain2, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_x(remain2, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)
    motor_y(slope, move_speed,1)
    laser(GPIO.HIGH)
    motor_x(grid, move_speed,1)
    laser(GPIO.LOW)
    
def enclose_f():
    motor_y(slope, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_x(remain3, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)

    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_x(remain3, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)

    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_x(remain3, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)

    laser(GPIO.HIGH)
    move_both(laser_speed,0,1)
    laser(GPIO.LOW)
    motor_x(remain3, move_speed,0)
    laser(GPIO.HIGH)
    move_both(laser_speed,0,0)
    laser(GPIO.LOW)

    laser(GPIO.HIGH)
    motor_x(grid, move_speed,1)
    laser(GPIO.LOW)
    
def cutting_f():
    motor_x(remain3, move_speed, 0)
    laser(GPIO.HIGH)
    motor_y(grid, laser_speed,0)
    laser(GPIO.LOW)
    motor_x(remain3, move_speed, 0)
    laser(GPIO.HIGH)
    motor_y(grid, laser_speed,1)
    laser(GPIO.LOW)
    motor_x(remain3, move_speed, 0)
    laser(GPIO.HIGH)
    motor_y(grid, laser_speed,0)
    laser(GPIO.LOW)
    motor_x(remain3, move_speed, 0)
    move_both(move_speed,1,1)