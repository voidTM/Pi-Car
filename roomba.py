from picar_4wd.speed import Speed
import RPi.GPIO as GPIO
import time, math
import picar_4wd as fc

import sys
import time

import scan as sc
from odometer import Duodometer

"""
    The basic driving and avoiding obstacles should be good for steps 1-3
"""
# 60 degree is about the closest servos
#scanning

        
# same as drive 1 but aims to use distance rather than status
def drive():
    speed = 30

    blocked = True

    tracker = Duodometer(4,24)
    tracker.start()

    while True:
        scan_list = sc.scan_step_dist()
        if not scan_list:
            continue
        scan_list = [200 if d < 0 else 200 if d > 200 else d for d in  scan_list] 

        #print(scan_list)
        ahead = scan_list[2:8]
        # coast clear full speed ahead        
        if min(ahead) > 35:
            #print("Coast Clear")
            blocked = False
            fc.forward(speed)
            continue
        elif min(scan_list) > 20:
            fc.forward(5)
            continue

        #print("need to stop")

        fc.stop()

        # cap at 200
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

        
        if not blocked:
            print(tracker.distance)
            blocked = True
            tracker.stop()

        if direction  == -1:
            print("turning left")
            fc.turn_left(10)
        elif direction  == 1:
            print("turning right")
            fc.turn_right(10)
        else:
            while(fc.get_distance_at(0) < 40):
                fc.backward(2)

    
def drive2():

    speed = 30

    blocked = False

    tracker = Duodometer(4,24)
    tracker.start()

    while True:
        scan_list = sc.scan_step_dist()
        if not scan_list:
            continue
        scan_list = [200 if d < 0 else 200 if d > 200 else d for d in  scan_list] 

        #print(scan_list)
        ahead = scan_list[2:8]
        # coast clear full speed ahead        
        if min(ahead) > 35:
            #print("Coast Clear")
            if  blocked:
                tracker.start()
                blocked = False
                
            fc.forward(speed)
            continue
        elif min(scan_list) > 20:
            fc.forward(5)
            continue

        #print("need to stop")

        fc.stop()

        # cap at 200
        left = scan_list[:5]
        right = scan_list[5:]

        # -1 = turn left, 0 forward, 1 turn right
        direction = 0
        target = 40
        print(left, right)
        if(sum(left) > sum(right)):
            direction = -1
            target = max(left) - 5
        elif(sum(left) < sum(right)):
            direction = 1
            target = max(right) - 5
        else:
            direction = 0

        
        if not blocked:
            print(tracker.distance)
            blocked = True
            tracker.stop()
        

        if direction  == -1:
            print("turning left")
            while(fc.get_distance_at(0) < target):
                fc.turn_left(10)
        elif direction  == 1:
            print("turning right")
            while(fc.get_distance_at(0) < target):
                fc.turn_right(10)
        else:
            while(fc.get_distance_at(0) < target):
                fc.backward(2)


if __name__ == "__main__":
    try: 
        drive()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
