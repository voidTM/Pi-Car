from picar_4wd.speed import Speed
import RPi.GPIO as GPIO
import time, math
import picar_4wd as fc

import sys
import time
import logging

import scanner
from odometer import Duodometer

"""
    The basic driving and avoiding obstacles should be good for steps 1-3
"""
# 60 degree is about the closest servos
#scanning



# picar drives around like a roomba without any  
def roomba(speed = 20):
    blocked = True
    while True:
        
        # get scan by distance
        scan_list = scanner.scan_step_dist()
        if not scan_list:
            continue

        # the preprocessing limits the max distance to 200cm
        # since any -2 means no response set the value to 200cm
        scan_list = [200 if d == -2 else d for d in  scan_list] 

        ahead = scan_list[2:8]

        # coast clear full speed ahead        
        if min(ahead) > 20:
            fc.forward(speed)
            continue

        logging.info("Too close stopping")
        fc.stop()

        # cap at 200
        right = scan_list[:5]
        left = scan_list[5:]

        # -1 = turn left, 0 forward, 1 turn right
        direction = 0
        
        # evaluates which direction turn
        # turns in the direction with the most open space

        if(sum(right) > sum(left)):
            direction = -1
        elif(sum(right) < sum(left)):
            direction = 1
        else:
            direction = 0

        
        print(sum(left), sum(right))
        print ( direction)

        if direction  == 1:
            logging.info("Turning right")
            fc.turn_right(10)
            time.sleep(1)
            fc.stop()
        elif direction  == -1:
            logging.info("Turning Right")
            fc.turn_left(10)
            time.sleep(1)
            fc.stop()
        else:
            while(fc.get_distance_at(0) < 30):
                logging.info("too close backing up")

                fc.backward(2)


def roomba1(speed = 20):

    while True:
        
        # get scan by distance
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        # the preprocessing limits the max distance to 200cm
        # since any -2 means no response set the value to 200cm

        ahead = scan_list[2:8]

        # coast clear full speed ahead        
        if min(ahead) > 1:
            fc.forward(speed)
            continue

        logging.info("Too close stopping")

        # cap at 200
        left = scan_list[:5]
        right = scan_list[5:]

        # -1 = turn left, 0 forward, 1 turn right
        direction = 0
        
        # evaluates which direction turn
        # turns in the direction with the most open space

        if(sum(left) > sum(right)):
            direction = -1
        elif(sum(left)  < sum(right)):
            direction = 1
        else:
            direction = 0


        if direction  == 1:
            logging.info("Turning Left")
            fc.turn_left(20)
            time.sleep(1)
            
        elif direction  == -1:
            logging.info("Turning Right")
            fc.turn_right(20)
            time.sleep(1)
        else:
            while(fc.get_distance_at(0) < 30):
                logging.info("too close backing up")

                fc.backward(2)

# aims for more accuracte angle    
def roomba2():

    speed = 10

    blocked = False


    while True:
        scan_list = scanner.scan_step_dist()
        if not scan_list:
            continue
        scan_list = [200 if d == -2 else d for d in  scan_list] 

        #print(scan_list)
        ahead = scan_list[2:8]
        # coast clear full speed ahead        
        print(ahead)
        if min(ahead) > 35:
            #print("Coast Clear")
            if  blocked:
                blocked = False
                
            fc.forward(speed)
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
            target = max(left) - 20
        elif(sum(left) < sum(right)):
            direction = 1
            target = max(right) - 20
        else:
            direction = 0

        
        if not blocked:
            blocked = True
        

        if direction  == -1:
            print("turning left")
            while(fc.get_distance_at(0) < target):
                fc.turn_left(10)
            fc.stop()
        elif direction  == 1:
            print("turning right")
            while(fc.get_distance_at(0) < target):
                fc.turn_right(10)
            fc.stop()

        else:
            while(fc.get_distance_at(0) < target):
                fc.backward(2)
            fc.stop()

        


if __name__ == "__main__":
    try: 
        logging.basicConfig(filename='roomba_drive.log', level=logging.INFO)
        roomba()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
