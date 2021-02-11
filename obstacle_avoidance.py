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
STEP = 18
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
step_count = ANGLE_RANGE//STEP

# degrees are from max -> min
nearby_dist = [0] * 10


# does a complete 180 scan:

def full_scan():
    global nearby_dist, STEP, step_count

    current_angle = max_angle
    for i in range(0, step_count, STEP):        
        nearby_dist[i] = fc.get_distance_at(current_angle)
        current_angle -= STEP

    print(nearby_dist)
        


def drive():
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
            time.sleep(10)
            scan_dist = 20
            speed = 30
            fc.forward(speed)



def drive2():
    
    go = 2
    scan_angles = [0, -20, -40, -20, 0, 20, 40, 20]

    while go > 0:
        #scan
        next_angle = 0

        # drive forward
        fc.forward(30)
        angle_log = []
        while(min(scan_list) > 0):
            fc.get_status_at(scan_angles[next_angle], ref1 = 35) < 1
            next_angle = (next_angle + 1) % 8
            angle_log.append(next_angle)

        fc.stop()
        print(angle_log)
        angle_log = []
        time.sleep(5)

        fc.backward(10)
        while(fc.get_status_at(scan_angles[next_angle], ref1 = 35) < 1):
            next_angle = (next_angle + 1) % 4
        
        fc.stop()
        time.sleep(5)

        fc.turn_right(10)
        while(fc.get_status_at(scan_angles[next_angle], ref1 = 50) < 2):
             next_angle = (next_angle + 1) % 4


# aka don't follow me
def drive3():
    speed = 30
    while True:
        scan_list = fc.scan_step(35)
        # print(scan_list)
        if not scan_list:
            continue
        
        # coast clear full speed ahead        
        print(scan_list)
        print(min(scan_list))
        if min(scan_list) > 1:
            print("Coast Clear")
            fc.forward(speed) 
        elif min(scan_list) == 1:
            print("objects nearby")
            fc.stop()
        else:

            fc.stop()
            print(scan_list)
            scan_list = [str(i) for i in scan_list]
            scan_list = "".join(scan_list)

            paths = [u for x in scan_list.split("0") for u in (x, "0")]

            print(paths)

            #get index to largest group

            i = paths.index(max(paths))
            print("paths ", paths)
            print(i)
            
            pos = scan_list.index(paths[i])

            # look for mid?
            pos += (len(paths[i]) - 1) / 2
            # pos = int(pos)
            delta = len(scan_list) / 3
            # delta *= us_step/abs(us_step)

            print(pos, delta)

            # turn away from obstacles
            
            if pos < delta:
                fc.turn_left(speed // 2)
            elif pos > 2 * delta:
                fc.turn_right(speed // 2)
            else:
                if scan_list[int(len(scan_list)/2-1)] == "0":
                    
                    fc.backward(speed)
                else:
                    fc.forward(speed)
            


def drive4():
    speed = 30
    scan_dist = 35
    
    while True:
        scanned = fc.scan_step(scan_dist)
        if not scanned:
            continue
        print(scanned)
        if(min(scanned) == 0):
            fc.stop()
        

        


if __name__ == "__main__":
    try: 
        full_scan()
        drive3()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
