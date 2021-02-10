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


def forward(speed):
    no_obstacle = True
    fc.forward(speed)
    while no_obstacle:
        scan_stat = fc.get_status_at(0)

        if scan_stat < 1:
            no_obstacle = False


def backup(speed):
    # time.sleep(2)
    fc.backward(speed)
    for i in range(10):
        time.sleep(0.1)
    fc.stop()

# find new direction
def turn(speed):
    blocked = True
    while blocked:
        
        fc.turn_right(speed)


#scanning
ANGLE_RANGE = 180
STEP = 20
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
step_count = ANGLE_RANGE/STEP

# degrees are from max -> min
scan_list = [0] * 9


# does a complete 180 scan:

def full_scan():
    global scan_list, STEP, step_count

    current_angle = max_angle
    for i in range(0, step_count, STEP):        
        scan_list[i] = fc.get_distance_at(current_angle)
        current_angle -= STEP


def drive():
    
    go = True
    current_angle = 0
    
    while go:
        #scan
        fc.forward(speed)





def drive2():
    speed = 30
    scan_dist = 20
    while True:
        scan_list = fc.scan_step(scan_dist)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2,2,2,2]:
            scan_dist = 50
            speed = 10
            
            
            fc.turn_right(speed)
        else:
            scan_dist = 20
            speed = 30
            fc.forward(speed)


if __name__ == "__main__":
    try: 
        full_scan()
        drive2()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
