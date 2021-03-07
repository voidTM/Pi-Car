
import numpy as np
import matplotlib.pyplot as plt
import sys
from PIL import Image


import time, math
import picar_4wd as fc

import utils
from odometer import Duodometer
import scanner
from gps import GPS
from car import Car


# check to see the picar is moving properly
def move_test():

    picar = Car()
    print("turning left")
    picar.turn_left(90)
    time.sleep(1)
    print("turning right")
    picar.turn_right(90)
    time.sleep(1)
    print("driving forward")
    picar.drive_forward(20)
    time.sleep(1)
    print("driving backward")
    picar.drive_backward(20)


def atestempty():
    grid = np.zeros([20,20], dtype = int)

    t = GPS()
    t.load_grid(grid, start_x = 10, start_y = 0)
    instructions = t.set_navigation_goal((19, 10))

    # while not at target
    while(len(instructions) > 0):
        # convert instructions to polar
        step = instructions.pop()
        print(step)


# drives forward until blocked
def drive_n_stop(speed: int = 10):
    clear = True
    fc.forward(speed)

    while clear:
        # scan list returns false until a full 180 deg scan is performed.
        scan_list = fc.scan_step(20)
        if not scan_list:
            continue

        ahead = scan_list[2:8]
        if min(ahead) < 2:
            clear = False
            fc.stop()

# scans the surroundings and saves the results to file
def stationary_scan_test():
    grid = np.zeros([50,50], dtype = int)

    t = GPS()
    t.load_grid(grid, resolution = 1, start_x = 25, start_y = 0)


    # performs a full 180 deg scan at 5 deg intervals
    obstacles = scanner.mapping_scan()

    # populate map with obstacles
    for obst in obstacles:
        picar_orientation = 0
        
        # actual orientation = picar_orientation + obstacle_scan angle
        orientation = obst[0] + picar_orientation

        t.add_relative_obstacle(orientation = obst[0], distance = obst[1])

    # save the scan results to file
    t.save_grid('maps/scan_result.out')


if __name__ == "__main__":
    try: 
        stationary_scan_test()
        

    finally: 
        fc.stop()
        # resets ultrasonic scanner to 0.
        fc.get_distance_at(0)
