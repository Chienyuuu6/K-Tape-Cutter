import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# Define the sequence for the 4-phase stepper motor
# You may need to adjust the sequence based on the motor's datasheet
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

def x_motor(steps, direction):
    # Define the GPIO pins for the stepper motor
    x_in1 = 18
    x_in2 = 23
    x_in3 = 24
    x_in4 = 25
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(x_in1, GPIO.OUT)
    GPIO.setup(x_in2, GPIO.OUT)
    GPIO.setup(x_in3, GPIO.OUT)
    GPIO.setup(x_in4, GPIO.OUT)
    move_stepper(x_in1,x_in2,x_in3,x_in4,steps,direction)
    
def y_motor(steps, direction):
    y_in1 = 5
    y_in2 = 16
    y_in3 = 20
    y_in4 = 21
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(y_in1, GPIO.OUT)
    GPIO.setup(y_in2, GPIO.OUT)
    GPIO.setup(y_in3, GPIO.OUT)
    GPIO.setup(y_in4, GPIO.OUT)
    move_stepper(y_in1,y_in2,y_in3,y_in4,steps,direction)
    
    
    
# Function to move the stepper motor
def move_stepper(in1, in2, in3, in4, steps, direction):   

    if (direction==0):
        for _ in range(steps):
            for i in range(8):
                GPIO.output(in1, seq[i][0])
                GPIO.output(in2, seq[i][1])
                GPIO.output(in3, seq[i][2])
                GPIO.output(in4, seq[i][3])
                time.sleep(0.001)
    else:
        for _ in range(steps):
            for i in range(8):
                GPIO.output(in4, seq[i][0])
                GPIO.output(in3, seq[i][1])
                GPIO.output(in2, seq[i][2])
                GPIO.output(in1, seq[i][3])
                time.sleep(0.001)
                



while(True):

    if(str(input('x or y:')) == "x"):    
        direction = int(input('forward(0) or backward(1):'))
        steps = int(input('How many steps:'))
        x_motor(steps,direction)

    else:    
        direction = int(input('forward(0) or backward(1):'))
        steps = int(input('How many steps:'))
        y_motor(steps,direction)
        
    if(int(input("continue(1) or not(0)"))==0):
        GPIO.cleanup()
        break


        