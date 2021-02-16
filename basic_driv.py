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

import numpy as np
# 60 degree is about the closest servos
#scanning
ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = 60
min_angle = -60
step_count = ANGLE_RANGE//STEP

# degrees are from max -> min        
scan_status = {}
scan_dist = {}

# each bit on the map should be 5 cm
bit_map = np.zeros((100, 100))
current_pos = [50,0]

def full_scan(ref1, ref2):
    global current_angle, us_step, scan_status,  scan_dist
    
    scan_status = {}
    for angle in range(min_angle, max_angle + 1, 12):
        scan_status[angle] = fc.get_status_at(angle, ref1, ref2)
        scan_dist[angle] = fc.get_distance_at(angle)
    
    print(scan_dist)
    return scan_status


# scans the next angle
def my_step_scan(ref1 = 10, ref2 = 35):
    global scan_list, current_angle, us_step
    current_angle += us_step
    # switches directions for angle
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    
    #dist = get_distance_at(current_angle)
    status = get_status_at(current_angle, ref1=ref1, ref2= ref2)#ref1

    #scan_list[i] = status
    return (current_angle, status)


def map_dist():

    global bit_map, scan_dist       
    print(scan_dist)
    for angle in scan_dist:
        rad_angle = np.radians(angle)
        dist = scan_dist[angle]
        x = int(dist * np.sin(rad_angle)) - current_pos[0]
        y = int(dist * np.cos(rad_angle)) - current_pos[1]
        print(x,y)
        if abs(x) < 100 and abs(y) < 100:

            bit_map[x][y] = 1
    
    for row in bit_map:
        print(row)

# aka don't follow me
def drive():
    speed = 30

    scan_list = [0] * 10

    while True:
        scan_results = fc.scan_step(35)
        # print(scan_list)
        if not scan_results:
            continue
        
        print(scan_results)
        for i in range(0, len(scan_results)):
            scan_list[i] = scan_results[i]

        print(scan_list)
        # coast clear full speed ahead        
        if min(scan_list) > 1:
            print("Coast Clear")
            fc.forward(speed) 
        elif min(scan_list) == 1:
            print("objects nearby")
            fc.stop()
        else:

            fc.stop()
            print(scan_list)
            str_scan = [str(i) for i in scan_list]
            str_scan = "".join(str_scan)

            paths = [u for x in str_scan.split("0") for u in (x, "0")]

            print(paths)

            #get index to largest group

            i = paths.index(max(paths))
            print("paths ", paths)
            print(i)
            
            pos = str_scan.index(paths[i])

            # look for mid?
            pos += (len(paths[i]) - 1) / 2
            # pos = int(pos)
            delta = len(str_scan) / 3
            # delta *= us_step/abs(us_step)

            print(pos, delta)

            # turn away from obstacles
            
            if pos < delta:
                fc.turn_left(speed // 2)
            elif pos > 2 * delta:
                fc.turn_right(speed // 2)
            else:
                if str_scan[int(len(str_scan)/2-1)] == "0":
                    
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
        full_scan(35, 10)
        map_dist()
        
    finally: 
        fc.get_distance_at(0)
        fc.stop()
