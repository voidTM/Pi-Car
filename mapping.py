import time, math
import threading
import picar_4wd as fc
from odometer import Duodometer

import numpy as np
import matplotlib.pyplot as plt
import scanner
import drive as dr
from scipy.interpolate import interp1d


# each bit on the map should be 5 cm
resolution = 5
# mid point of map
car_pos = np.array([100,100])
# -1 for unknown
# 0 for clear
# 1 for obstacle
bit_map = np.full((200, 200), 0, dtype = int)



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



def interpolate(x1, y1, x2, y2):
    # interpolate across the x axis
    xRange = np.arange(x1, x2)
    fx = interp1d([x1,x2], [y1,y2])

    if x1 > x2:
        xRange = np.arange(x2, x1)
        fx = interp1d([x2,x1], [y2,y1])

    yRange = fx(xRange)
    print(x2,y2)
    print(xRange,yRange)    

    yRange = yRange.astype(int)

    return np.array([xRange,yRange]).T


def fill_between(grid, x1, y1, x2, y2, value):
    
    interpolated_values = interpolate(x1, y1, x2, y2)
    
    if interpolated_values.size == 0:
        print("failed interpolation", x2,y2)

    for v in interpolated_values:
        if in_map_bounds(grid, v[0], v[1]):
            grid[v[1]][v[0]] = value

    return grid


# 2 datapointa are 3 or fewer datapoints away join them?


# returns a list of nearby points if any
def nearby_points(grid, obs_x, obs_y):

    # 20cm should give enough space for a picar to pass through
    radius = 20 // resolution

    nearby = np.array([])

    # set search boundaries
    minx = max(obs_x - radius, 0)
    miny = max(obs_y - radius, 0)
    maxx = min(obs_x + radius, len(grid) - 1)
    maxy = min(obs_y + radius, len(grid) - 1)

    for x in range(obs_x - radius, obs_x + radius):
        for y in range(obs_y - radius, obs_y + radius):
            if grid[x][y] == 1:
                continue

    return nearby

# adds scanned information to map\s?
def map_obstacles(grid, car_pos, car_orientation, obstacle_pos):
   

    global resolution
    for obstacle in obstacle_pos:
        # 1 convert polar to carteisan

        obs_x, obs_y = pol2cart(obstacle[0] + car_orientation, obstacle[1])

        # 2 calculate offset from car posistion
        obs_x = int(obs_x / resolution) + car_pos[0]
        obs_y = int(obs_y / resolution) + car_pos[1]
        # map if not out of bounds

        #print(obs_x, obs_y)
        if in_map_bounds(grid, obs_x, obs_y):
            grid[obs_x][obs_y] = 1

        # check for nearby points
    
    
    np.savetxt('maps/testmap.out', bit_map,fmt='%i', delimiter=',')

    return grid

def map_n_drive():
    global car_pos, bit_map

    car_theta = 0
    curr_distance = 0
    for i in range(0, 2):
        currObstacles = scanner.mapping_scan()

        map_obstacles(bit_map, car_pos, car_theta, currObstacles)

        theta, distance_driven = dr.drive_dist(speed = 5, distance = 20, theta =car_theta)
        
        # update car position
        delta_X, delta_Y = pol2cart(theta, distance_driven)
        car_pos[0] = int(delta_X / resolution) + car_pos[0]
        car_pos[1] = int(delta_Y / resolution) + car_pos[1]
        print(car_pos)

if __name__ == "__main__":
    try: 
        
        map_n_drive()


    finally: 
        fc.get_distance_at(0)
        fc.stop()

        np.savetxt('maps/testmap.out', bit_map,fmt='%i', delimiter=',')
