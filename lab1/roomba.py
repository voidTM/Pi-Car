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
    The basic driving and avoiding obstacles for Part 1 of lab
"""

# picar drives around like a roomba without any  
def roomba(speed = 10):

    while True:
        
        # get scan by distance
        scan_list = scanner.scan_step_dist()
        if not scan_list:
            continue

        # the preprocessing limits the max distance to 200cm
        # since any -2 means no response set the value to 200cm
        scan_list = [200 if d == -2 else d for d in  scan_list] 

        # readings that are infront on the Picar
        # -54 degrees to 54 degrees
        ahead = scan_list[2:7]

        # coast clear full speed ahead        
        if min(ahead) > 35:
            fc.forward(speed)
            continue

        logging.info("Too close stopping")
        fc.stop()


        left = scan_list[:5]
        right = scan_list[5:]

        # -1 = turn left, 0 forward, 1 turn right
        direction = 0
        # evaluates which direction turn
        # turns in the direction with the most open space

        if(sum(right) > sum(left)):
            direction = 1
        else:
            direction = -1

        
        #print(sum(left), sum(right))
        #print( direction)

        if direction  == 1:
            logging.info("Turning right")
            fc.turn_right(speed)
        elif direction  == -1:
            logging.info("Turning left")
            fc.turn_left(speed)
        


if __name__ == "__main__":
    try: 

        roomba()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
