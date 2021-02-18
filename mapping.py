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
import matplotlib.pyplot as plt

# 60 degree is about the closest servos
# think of arks
#scanning
ANGLE_RANGE = 180
STEP = 10
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = 90
min_angle = -90
step_count = ANGLE_RANGE//STEP

# degrees are from max -> min        
scan_status = {}
scan_dist = {}

# each bit on the map should be 5 cm
bit_map = np.zeros((101, 101))
current_pos = (50,0)
relative_map = np.zeros((100,100,100))


# note ultrasonic are waves and thus not entirely accurate
def full_scan(ref1, ref2):
    global current_angle, us_step, scan_status,  scan_dist
    fc.get_status_at(min_angle)
    time.sleep(1)
    scan_status = {}
    for angle in range(min_angle, max_angle + 1, 10):
        time.sleep(1)
        scan_status[angle] = fc.get_status_at(angle, ref1, ref2)
        scan_dist[angle] = fc.get_distance_at(angle)
        print(angle, scan_dist[angle])

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


# step_scan but returns the distance instead
def step_scan_dist():
    global scan_dist, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP

    dist = fc.get_distance_at(current_angle)

    scan_dist.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_dist.reverse()
        # print(scan_list)
        tmp = scan_dist.copy()
        scan_dist = []
        return tmp
    else:
        return False


def offsetXY(obstacleX, obstacleY, vehicleX, vehicleY, theta = -1):
    if theta >= 0:
        outputX = vehicleX - obstacleX
    else:
        outputX = vehicleX + obstacleX

    outputY = (vehicleY * 2) + obstacleY
    
    return outputX, outputY


# finds the relative locations of an object
# and returns a numpy array of coordinates
def find_obstacles(carX = 0, carY = 0):
    global scan_dist
    
    # find the location assuming car is (0,0)
    relativeLocations = []

    for angle in scan_dist:
        # convert to radians
        radAngle = np.radians(angle)
        dist = scan_dist[angle]
        x = int(dist * np.sin(radAngle))        
        y = int(dist * np.cos(radAngle))
        relativeLocations.append([x,y])

    
    l = np.array(relativeLocations).T
    print(list(l))
    return l



def fill_map(map, x_bounds, y_bounds, value = 10):

    # bind the x range between 0 and 99
    lower_x = max(x_bounds[0], 0)
    upper_x = min(x_bounds[1], 99)

    x = np.arange(lower_x, upper_x)

    if(x.size == 0):
        print("x is out of map bounds")
        return 

    y = np.interp(x, x_bounds, y_bounds)

    print(x)
    print(y)
    """
    xy = np.array([x,y])
    print(xy.shape)
    print(xy)
    # fill in 1 column by column
    for i in range(len(y)):
        continue
    """

    


# adds scanned information to map\s?
def map_dist():

    global bit_map, scan_dist
    prev_point = [0,0]     
    x_bounds = [0,0]
    y_bounds = [0,0] 
    obstacle_locations = []
    for angle in scan_dist:
        rad_angle = np.radians(angle)
        dist = scan_dist[angle]
        
        x =  50 + int(dist * np.sin(rad_angle))
        y = int(dist * np.cos(rad_angle))

        if(prev_point[0] < x):
            x_bounds = np.array([prev_point[0], x])
            y_bounds = np.array([prev_point[1], y])
        else:
            x_bounds = np.array([x, prev_point[0]])
            y_bounds = np.array([y, prev_point[1]])
        print(x,y)
        #fill_map(bit_map, x_bounds, y_bounds, 1)
        prev_point = [x,y]
        obstacle_locations.append([x,y])

    obstacles = np.array(obstacle_locations)
    print(obstacles)
    obstacles = obstacles.T

    x = plt.plot(obstacles[0], obstacles[1], 'o')


    np.savetxt('front_bitmap.txt', x, delimiter=' ')
    

if __name__ == "__main__":
    try: 
        full_scan(35, 10)
        find_obstacles()    
    finally: 
        fc.get_distance_at(0)
        fc.stop()
