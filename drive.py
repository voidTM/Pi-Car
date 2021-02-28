import time, math
import picar_4wd as fc

import sys
import threading
import signal
from collections import deque
from queue import Queue

# self defined
import scanner
import utils
from car import Car
from odometer import Duodometer
from gps import GPS

import detect as picam



# drives around without any mapping, but has basic obstacle avoidance
def roomba(speed = 10):

    while True:
        
        # get scan by distance
        scan_list = scanner.scan_step_dist()
        if not scan_list:
            continue

        # preprocess scanlist
        scan_list = [200 if d == -2 else 200 if d > 200 else d for d in  scan_list] 


        ahead = scan_list[3:7]

        # coast clear full speed ahead        
        if min(ahead) > 35:
            #print("Coast Clear")
            blocked = False
            fc.forward(speed)
            continue

        #print("need to stop")

        fc.stop()

        # cap at 200
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
            print("Turning right")
            fc.turn_right(10)
        elif direction  == -1:
            print("Turning Right")
            fc.turn_left(10)
        else:
            while(fc.get_distance_at(0) < 30):
                logging.info("too close backing up")

                fc.backward(2)

# drives toward a certain target on a grid
def drive_target(target:tuple):

    car_theta = 0
    curr_distance = 0
    nav = GPS(map_width = 30, map_length = 30, resolution = 10, start_x = 15, start_y = 0)
    picar = Car()
    
    at_destination = False

    while(not at_destination):

        print("blocked!, rerouting")
        # scan for obstacles
        obstacles = scanner.mapping_scan()
        print(obstacles)
        for obst in obstacles:
            abs_orient = obst[0] + picar.orientation
            nav.add_relative_obstacle(orientation = abs_orient, distance = obst[1])
            
        instructions = nav.set_navigation_goal(target)
        
        at_destination = drive_instructions(picar, nav, instructions)
        

# drive according to instructions until blocked or finished
def drive_instructions(picar: Car, nav:GPS, instructions:deque):

    # while not at target
    while(len(instructions) > 0):
        # convert instructions to polar
        step = instructions.popleft()
        print("directions: ", step)
                
        direction = step[0] - picar.orientation
        direction = (direction + 180) % 360 - 180
        #print("turning angle", direction)

        
        driven = 0
        # change direction if needed
        if direction > 0: 
            picar.turn_right(direction)
        elif direction < 0:
            picar.turn_left(abs(direction))

        if step[1] >= 0:
            driven = picar.drive_forward(distance = step[1])
        else:
            driven = picar.drive_backward(distance = abs(step[1]))

        nav.update_postion(distance = int(driven), orientation = picar.orientation)
        print( "curr position", nav.position)

        # if blocked rerout
        if driven < step[1]:
            return False

    return True

    
def drive_instructions2(picar: Car, nav:GPS, instructions:deque, obstacles: Queue):
    pass


if __name__ == "__main__":
    try: 
        roomba()
        #drive_target((0, 10))
        #turn_test()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
