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
from car import PiCar

from odometer import Duodometer
from gps import GPS

import detect as picam



# check to see the picar is moving properly
def move_test():

    picar = Car()

    print("turning left")
    picar.turn_left(90)
    time.sleep(1)
    print("turning right")
    picar.turn_right(180)
    time.sleep(1)
    print("turning left")
    picar.turn_left(90)
    time.sleep(1)

    print("driving forward")
    picar.drive_forward(20)
    time.sleep(1)
    print("driving backward")
    picar.drive_backward(20)


# drives forward until blocked
def drive_n_stop(speed: int = 10):
    clear = True
    fc.forward(speed)
    while clear:
        scan_list = fc.scan_step()
        if not scan_list:
            continue

        ahead = scan_list[2:8]
        # coast clear full speed ahead        
        if min(ahead) < 2:
            #print("Coast Clear")
            clear = False
            fc.stop()



# drives toward a certain target on a grid
def drive_target(nav: GPS,  target: tuple):

    car_theta = 0
    curr_distance = 0
    picar = Car()
    
    at_destination = False

    while(not at_destination):

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



# drives to a destination 
def drive_picar():
    nav = GPS(map_width = 100, map_length = 100, resolution = 10, start_x = 50, start_y = 0)
    target = (50, 20)

    c = PiCar(nav)

    c.drive_target(target)

    del c


# drives forward until blocked
def drive_n_stop(speed: int = 5):
    clear = True
    fc.forward(speed)

    while clear:
        # scan list returns false until a full 180 deg scan is performed.
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        ahead = scan_list[2:8]
        if min(ahead) < 2:
            clear = False
            fc.stop()




if __name__ == "__main__":
    try:

        #
        # move_test()
        drive_picar()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
