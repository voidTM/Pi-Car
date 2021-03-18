
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



# scans the surroundings and saves the results to file
def stationary_scan_test():
    scan_list = scanner.scan_step_dist()

    while not scan_list:
        scan_list = scanner.scan_step_dist()

    print(scan_list)

    grid = np.zeros([50,50], dtype = int)

    t = GPS()
    t.load_grid(grid, resolution = 2, start_x = 25, start_y = 0)


    # performs a full 180 deg scan at 5 deg intervals
    obstacles = scanner.mapping_scan()
    print(obstacles)
    #obstacles[:,0] *= -1
    #print(obstacles)

    # populate map with obstacles
    for obst in obstacles:
        picar_orientation = 90
        
        # actual orientation = picar_orientation + obstacle_scan angle
        orientation = obst[0] + picar_orientation

        t.add_relative_obstacle(orientation = obst[0], distance = obst[1])

    # save the scan results to file
    t.save_grid('maps/1object_scan_result.out')

    return t

def astest():
    
    t = GPS()
    
    obstacles = scanner.mapping_scan()
    print(obstacles)
    #obstacles[:,0] *= -1
    #print(obstacles)

    # populate map with obstacles
    for obst in obstacles:
        picar_orientation = 90
        
        # actual orientation = picar_orientation + obstacle_scan angle
        orientation = obst[0] + picar_orientation

        t.add_relative_obstacle(orientation = obst[0], distance = obst[1])

    instructions = t.set_navigation_goal((19, 10))

    # while not at target
    while(len(instructions) > 0):
        # convert instructions to polar
        step = instructions.pop()
        print(step)


if __name__ == "__main__":
    try: 
        #stationary_scan_test()

        astest()

        #drive_n_stop()
        #sensor_test()
        #move_test()
    finally: 
        fc.stop()
        # resets ultrasonic scanner to 0.
        fc.get_distance_at(0)
