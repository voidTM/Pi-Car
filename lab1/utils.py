import math
import numpy as np

# various utiliy functions that may be useful for calcuations



def angle_to_dist(angle, radius = 7):
    
    rot = angle / 360
    circumference = 2 * radius * math.pi

    return rot * circumference
    
def dist_to_angle(dist, radius = 7):
    circumference = 2 * radius * math.pi

    # only last rotation matters
    rot = (dist // circumference) - (dist / circumference)

    return rot * 360
    




# checks how far the car has rotated
def rotation(curr_theta, start_dist, end_dist):

    # distance between front wheels ia about 14cm    
    d = 14 
    r = 7
    circumference = d * math.pi 
    
    radians  = (end_dist - start_dist) / r


    # convert to degrees
    deg = radians * (180 / math.pi)

    return  int(curr_theta + deg) % 360


def pol2cart(angle, dist):
    rad_angle = np.radians(angle)
        
    x = dist * np.sin(rad_angle)
    y = dist * np.cos(rad_angle)
    return (x, y)


def cart2pol(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y1 - y2



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
