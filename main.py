import cutter as k
import qrcode as qr
import RPi.GPIO as GPIO

print('K-Tape Cutter start working!')


# tape format
# UU
def tape1(length):

    k.roller()
    k.onclose_u()
    
    length -=1
    while (length>0):
        k.roller()
        length -=1
    k.enclose_u()


# UY
def tape2(length, inner_length):

    k.roller()
    k.onclose_u()

    length = length - inner_length -1

    while (length > 0):
        k.roller()
        length-=1

    k.motor_x(366, 0.001, 0)
    k.laser(GPIO.HIGH)
    while(inner_length>0):
        k.roller()
        inner_length-=1
    k.laser(GPIO.LOW)
    k.motor_x(366, 0.001, 1)
    
    k.enclose_y()



# YY
def tape3(length, inner_length):

    k.roller()
    k.onclose_y()
    
    k.motor_x(366, 0.001, 0)
    k.laser(GPIO.HIGH)

    inner1=inner_length
    while (inner1-1>0):
        k.roller()
        inner1-=12
    k.laser(GPIO.LOW)

    middle=length-(inner_length*2)
    while (middle>0):
        k.roller()
        middle-=1

    k.laser(GPIO.HIGH)
    inner2=inner_length
    while (inner2>0):
        k.roller()
        inner2-=1
    k.laser(GPIO.LOW)

    k.motor_x(366, 0.001, 1)
    k.enclose_y()



# UF
def tape4(length, inner_length):

    k.roller()
    k.onclose_u()

    length = length - inner_length -1

    while (length > 0):
        k.roller()
        length-=1

    k.motor_x(366, 0.001, 0)
    k.laser(GPIO.HIGH)
    while(inner_length>0):
        k.roller()
        k.cutting_f()
        inner_length-=1
    k.laser(GPIO.LOW)
    k.motor_x(366, 0.001, 1)
    
    k.enclose_f()



def main():
            format, length, inner = qr.run()

            if(format=='tape1'):
                tape1(length)

            elif(format=='tape2'):
                tape2(length, inner)

            elif(format=='tape3'):
                tape3(length, inner)

            elif(format=='tape4'):
                tape4(length, inner)
        
            print('K-Tape Cutting finished!!')


if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print('K-Tape Cutter shut down!!')
            GPIO.cleanup()
            pass
            break
