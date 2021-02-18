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

from odometer import Duodometer


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

    speed3 = Speed(25)
    speed4 = Speed(4) 
    speed3.start()
    speed4.start()
    fc.turn_left(10)

    try:
        # nc.stop()
        for i in range(20):
            # speed_counter 
            # = 0
            print(speed3(), speed4())
            print(speed3.speed_counter, speed4.speed_counter)
            print(" ") 
            time.sleep(0.5)
    finally:
        speed3.deinit()
        speed4.deinit()
        fc.stop() 

def test2():
    odometer = Duodometer(4, 24)

    odometer.start()
    
    for i in range(0,20):
        time.sleep(1)
        print(odometer.distance)

    odometer.stop()


def test3():
    speed4 = Speed(25)
    speed4.start()
    # time.sleep(2)
    fc.forward(10)
    x = 0 # distance traveled
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

def scan_test():
    best = [fc.get_distance_at(0), 0]
    step_size = 10

    for current_angle in range(-90, 90, step_size):
        dist = fc.get_distance_at(current_angle)
        if dist > best[0]:
    
            best = [dist, current_angle]


    fc.get_distance_at(0)

    print(best)
    return best


# close to a 90 right turn on average
def turn_right(degrees):
    speed4 = Speed(4)
    speed4.start()
    dist = 0
    fc.turn_right(10)
    while(dist < 25):
        time.sleep(0.1)
        speed = speed4()
        dist += speed * 0.1
        print("%smm/s"%speed)
    print(dist)
    speed4.deinit()
    fc.stop()

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
        if key == "1":
            test1()
        elif key=="2":
            test2()
        elif key=="3":
            test3()
        elif key=="4":
            scan_test()
        elif key == "5":
            turn_test()
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






