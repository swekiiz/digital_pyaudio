import RPi.GPIO as GPIO
import time
import random
import math
GPIO.setmode(GPIO.BOARD)

PIN_CLK  = 3
PIN_DATA = 5
PIN_CLR  = 7

GPIO.setwarnings(False)
GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_DATA, GPIO.OUT)
GPIO.setup(PIN_CLR, GPIO.OUT)

def send_clk():
    GPIO.output(PIN_CLK, True)
    GPIO.output(PIN_CLK, False)

def send_clr():
    GPIO.output(PIN_CLR, True)
    GPIO.output(PIN_CLR, False)

def outSine():
    try:
        while True:
            
            #x = int(input("Enter code(16bit, 0-65535): "))
            #x = random.randint(0, 65536)
            for i in range(360):
                x = int(((math.sin(math.radians(i)) + 1) * (2**16-1)) // 2);
                #print(x, end=' : ')
                #stack = ""
                for i in range(16):
                    ## LSB -> MSB
                    GPIO.output(PIN_DATA, x & 1 )
                    #stack += bin(x)[-1]
                    x >>= 1
                    send_clk()
                #print("Sended:", stack[::-1])
                #time.sleep(1)
            #time.sleep(1)
    except:
        print("error")
        pass
    finally:
        GPIO.cleanup()

def outValue():
    try:
        while True:
            
            #x = int(input("Enter code(16bit, 0-65535): "))
            #x = random.randint(0, 65536)
            x = 2**16-1
            stack = ""
            for i in range(16):
                ## LSB -> MSB
                GPIO.output(PIN_DATA, x & 1 )
                send_clk()
                stack += bin(x)[-1]
                x >>= 1
            time.sleep(0.001)
            print("Sendeended:", stack[::-1])
            #time.sleep(1)
    except:
        print("error")
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    send_clr()
    outSine()
    #outValue()
