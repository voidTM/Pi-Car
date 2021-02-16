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


# 60 degree is about the closest servos
#scanning
ANGLE_RANGE = 180
STEP = 18
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
step_count = ANGLE_RANGE//STEP

# degrees are from max -> min
scan_list = [0] * 10
        

# scans the next angle
def my_step_scan(ref1, ref2):
    global scan_list, current_angle, us_step
    current_angle += us_step
    # switches directions for angle
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    
    dist = get_distance_at(current_angle)
    status = get_status_at(current_angle, ref1=ref1, ref2= ref2)#ref1

    #scan_list[i] = status
    return (current_angle, status)



# 20 should be the minimum distance

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
    
    speed = 30
    scan_dist = 20
    
    while True:
        scan_list = fc.scan_step(scan_dist)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        
        print(tmp)
        #nearby objects
        if(min(tmp) < 2):
            
            speed = 10
            

            fc.turn_right(speed)
        else:
            speed = 30
            fc.forward(speed)


# aka don't follow me
def drive3():
    speed = 30

    while True:
        scan_list = fc.scan_step(35)


        if not scan_list:
            continue
        
        ahead = scan_list[3:7]
        # coast clear full speed ahead        
        if min(scan_list) > 1:
            print("Coast Clear")
            continue
        elif min(scan_list) == 1:
            print("objects nearby")
            fc.forward(2) 
            
        print("need to stop")

        fc.backward(speed)
        time.sleep(1)
        fc.stop()

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

        time.sleep(10)   
        if pos < delta:
            print("turning left")
            fc.turn_left(speed // 2)
        elif pos > 2 * delta:
            print("turning right")
            fc.turn_right(speed // 2)
        else:
            if str_scan[int(len(str_scan)/2-1)] == "0":
                    
                fc.backward(5)
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
        drive2()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
