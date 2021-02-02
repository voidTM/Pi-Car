from picar_4wd.speed import Speed
import RPi.GPIO as GPIO
import time, math
import threading
import picar_4wd as fc

import sys
import tty
import termios
import asyncio
import time

power_val = 50
key = 'status'
print("If you want to quit.Please press q")


def foward(power:int, t:int):
    try:
        fc.forward(power)
        time.sleep(t)
    except:
        print("move failed")
    
    fc.stop()



def test1():
    # import fwd as nc 
    fc.forward(100)

    speed3 = Speed(25)
    speed4 = Speed(4) 
    speed3.start()
    speed4.start()
    try:
        # nc.stop()
        while 1:
            # speed_counter 
            # = 0
            print(speed3())
            print(speed4())
            print(" ") 
            time.sleep(0.5)
    finally:
        speed3.deinit()
        speed4.deinit()
        fc.stop() 

def test2():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while True:
        print(GPIO.input(12))
        time.sleep(0.001) 

def test3():
    speed4 = Speed(25)
    speed4.start()
    # time.sleep(2)
    fc.forward(10)
    x = 0
    for i in range(2):
        time.sleep(0.1)
        speed = speed4()
        x += speed * 0.1
        print("%smm/s"%speed)
    print("%smm"%x)
    speed4.deinit()
    fc.stop()

# test scanner
def ultrasonic_test():
    #scan_list = fc.scan_step(35)

    #tmp = scan_list[3:7]
    #print(scan_list)

    distance = fc.get_distance_at(0)
    print(distance) # should be in cm


def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def Keyborad_control():
    while True:
        global power_val
        key=readkey()
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)
        if key=='w':
            foward(power_val, 1)
        elif key=='a':
            fc.turn_left(power_val)
        elif key=='s':
            fc.backward(power_val)
        elif key=='d':
            fc.turn_right(power_val)
        elif key == "1":
            test1()
        elif key=="2":
            test2()
        elif key=="3":
            test3()
        elif key == "5":
            ultrasonic_test()
        else:
            fc.stop()
        if key=='q':
            print("quit")
            fc.stop()  
            break  
if __name__ == '__main__':
    try: 
        Keyborad_control()
    finally:
        fc.stop()






