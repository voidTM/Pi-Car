import picar_4wd as fc
from odometer import Duodometer

import numpy as np
import scanner
import utils

from gps import GPS
from scipy.interpolate import interp1d


# each bit on the map should be 5 cm
resolution = 5
# mid point of map
car_pos = np.array([100,100])
# -1 for unknown
# 0 for clear
# 1 for obstacle


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

