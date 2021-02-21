
import time, math
import picar_4wd as fc

import sys
import time

import scanner
import gps
from odometer import Duodometer

# goal is to track the car's position through motor movement.

# position in cm
starting_pos = []
prev_pos = []
curr_pos = [0,0] 

# speed is the same wether it turns left or right
turn_meter = Duodometer(12, 22)




# calculates the relative distance moved
def distance_moved(prev_dist):
    #ultrasonic reading2 - ultrasonic reading1   
    curr_dist = fc.get_distance_at(0)
    
    return curr_dist - prev_dist



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


def hybridAPathing():
    return