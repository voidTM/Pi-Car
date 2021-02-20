from picar_4wd.speed import Speed
import RPi.GPIO as GPIO
import time, math
import picar_4wd as fc

import sys
import time

import scanner
import gps
from odometer import Duodometer


def turn_target(scanned_distances):
    mid = len(scanned_distances) // 2

    left = scanned_distances[:mid]
    right = scanned_distances[mid:]

    target = 40 # target for open space
    direction = 0 #turn direction

    if(sum(left) > sum(right)):
        direction = -1
        target = max(left) - 5
    elif(sum(left) < sum(right)):
        direction = 1
        target = max(right) - 5
    else:
        direction = 0
    
    return direction, target
        

def turn(angle, power = 10):
    turn_dist = gps.angle_to_dist(angle)

    if angle < 0:
        while(fc.get_distance_at(0) < turn_dist):
            fc.turn_left(power)
    elif angle > 1:
        while(fc.get_distance_at(0) < turn_dist):
            fc.turn_right(power)
    else:
        while(fc.get_distance_at(0) < turn_dist):
            fc.backward(2)


# 20 should be the minimum distance

def drive_dist(speed = 30, distance= 40):

    blocked = False

    trip = Duodometer(4,24)
    trip.start()

    while trip.distance < distance:



        

        


if __name__ == "__main__":
    try: 
        drive2()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
