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
        print(scan_list)
        print(tmp)
        #nearby objects
        if(min(tmp) < 2):
            
            fc.stop()
            speed = 10
            

            time.sleep(10)
            fc.turn_right(speed)
        else:
            speed = 30
            fc.forward(speed)


# aka don't follow me
def drive3():
    speed = 30

    fc.forward(speed) 

    while True:
        scan_list = fc.scan_step(35)


        if not scan_list:
            continue
        print(scan_list)
        ahead = scan_list[3:7]
        # coast clear full speed ahead        
        if min(ahead) > 1:
            print("Coast Clear")
            fc.forward(speed)
            continue

        print("need to stop")

        while(fc.get_distance_at(0) < 30):
            fc.backward(2)

        fc.stop()
        time.sleep(5)
        str_scan = "".join([str(i) for i in scan_list])

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
            print("turning left")
            fc.turn_left(10)
        elif pos > 2 * delta:
            print("turning right")
            fc.turn_right(10)
        else:
            if int(str_scan[len(str_scan)//2-1]) < 2:
                    
                fc.backward(1)
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
        
def drive5():
    speed = 30

    fc.forward(speed) 

    while True:
        scan_list = fc.scan_step(35)


        if not scan_list:
            continue
        print(scan_list)
        ahead = scan_list[2:8]
        # coast clear full speed ahead        
        if min(ahead) > 1:
            print("Coast Clear")
            fc.forward(speed)
            continue

        print("need to stop")

        fc.stop()

        left = scan_list[:5]
        right = scan_list[5:]

        # -1 = turn left, 0 forward, 1 turn right
        direction = 0
        print(left, right)
        if(sum(left) > sum(right)):
            direction = -1
        elif(sum(left) < sum(right)):
            direction = 1
        else:
            direction = 0


        if direction  == -1:
            print("turning left")
            fc.turn_left(10)
        elif direction  == 1:
            print("turning right")
            fc.turn_right(10)
        else:
            while(fc.get_distance_at(0) < 50):
                fc.backward(2)

        


if __name__ == "__main__":
    try: 
        drive5()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
