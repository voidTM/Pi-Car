import time, math
import threading
import picar_4wd as fc
from odometer import Duodometer

import numpy as np
import matplotlib.pyplot as plt
import scanner
from scipy.interpolate import interp1d


# each bit on the map should be 5 cm
resolution = 5
# mid point of map
car_pos = np.array([100,100])
# -1 for unknown
# 0 for clear
# 1 for obstacle
bit_map = np.full((200, 200), 0, dtype = int)



def pol2cart(angle, dist):
    rad_angle = np.radians(angle)
        
    x = dist * np.sin(rad_angle)
    y = dist * np.cos(rad_angle)
    return (x, y)



def offsetXY(obstacleX, obstacleY, vehicleX, vehicleY, theta = -1):
    global resolution
    if theta >= 0:
        outputX = vehicleX - obstacleX
    else:
        outputX = vehicleX + obstacleX

    outputY = vehicleY + obstacleY
    
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


# loads a stored map
def load_map(filepath):
    print(filepath)



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

# check to see if obstacle is within map bounds
def in_map_bounds(grid, x, y):

    upper_bound = len(grid) - 1
    if x < 0 or x > upper_bound:
        return False 
    if y < 0 or y > upper_bound:
        return False
    
    return True

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

    for x in range(obs_x -)

    return nearby

# adds scanned information to map\s?
def map_obstacles(grid, car_pos, car_orientation, obstacle_pos):
   

    global resolution
    print(car_orientation)
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

    return grid

def set_obstacle(map, car_pos, orientation, obstacle_pos):
	# set the occupied cells when detecting an obstacle
	# grid:				ndarray [width,height]
	# car_pos:			[x y] pose of the car
	# orientation:      quaternion, orientation of the car
	global resolution
    

	if not car_range == 0.0:

		rotMatrix = numpy.array([[numpy.cos(euler[2]),   numpy.sin(euler[2])],
			                     [-numpy.sin(euler[2]),  numpy.cos(euler[2])]])
		obstacle = numpy.dot(rotMatrix,numpy.array([0, (car_range + position_sonar[0]) // resolution])) + numpy.array([off_x,off_y])


		# set probability of occupancy to 100 and neighbour cells to 50
		grid[int(obstacle[0]), int(obstacle[1])] = int(100)
		if  grid[int(obstacle[0]+1), int(obstacle[1])]   < int(1):
			grid[int(obstacle[0]+1), int(obstacle[1])]   = int(50)
		if  grid[int(obstacle[0]), 	 int(obstacle[1]+1)] < int(1):
			grid[int(obstacle[0]),   int(obstacle[1]+1)] = int(50)
		if  grid[int(obstacle[0]-1), int(obstacle[1])]   < int(1):
			grid[int(obstacle[0]-1), int(obstacle[1])]   = int(50)
		if  grid[int(obstacle[0]),   int(obstacle[1]-1)] < int(1):
			grid[int(obstacle[0]),   int(obstacle[1]-1)] = int(50)

		t = 0.5
		i = 1
		free_cell = numpy.dot(rotMatrix,numpy.array([0, t*i])) + numpy.array([off_x,off_y])
		while grid[int(free_cell[0]), int(free_cell[1])] < int(1):
			grid[int(free_cell[0]), int(free_cell[1])] = int(0)
			free_cell = numpy.dot(rotMatrix,numpy.array([0, t*i])) + numpy.array([off_x,off_y])
			i = i+1;


def map_n_drive():
    global theta, car_pos, bit_map

    meter = Duodometer(4,24)
    meter.start()
    theta = 0
    prevDistance = 0

    for i in range(0, 1):
        currObstacles = scanner.mapping_scan()
        currDistance = meter.distance

if __name__ == "__main__":
    try: 
        
        meter = Duodometer(4,24)
        car_theta = 0
        meter.start()
        prevDistance = 0

        for i in range(0, 1):
            currObstacles = scanner.mapping_scan(step = 2)
            currDistance = meter.distance
            


            map_obstacles(bit_map, car_pos, car_theta, currObstacles)


    finally: 
        fc.get_distance_at(0)
        fc.stop()

        np.savetxt('maps/testmap.out', bit_map,fmt='%i', delimiter=',')
