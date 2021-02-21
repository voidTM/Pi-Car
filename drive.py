from picar_4wd.speed import Speed
import RPi.GPIO as GPIO
import time, math
import picar_4wd as fc

import sys
import time

import scanner
import gps
from odometer import Duodometer


# speed is the same wether it turns left or right
turn_meter = Duodometer(12, 22)

def turn_right(power = 5, angle):
    
    dist = angle_to_dist(angle)
    turn_meter.start()
    fc.turn_right(power)
    while(turn_meter.distance < dist):
        continue
    
    fc.stop()
    turn_meter.stop()

def turn_left(power = 5, angle):
    dist = angle_to_dist(angle)
    turn_meter.start()
    fc.turn_left(power)
    while(turn_meter.distance < dist):
        continue
    
    fc.stop()
    turn_meter.stop()

def drive_forward(power = 5, distance = 10):
    dist = angle_to_dist(angle)
    meter.start()
    fc.forward(power)
    while(turn_meter.distance < dist and fc.get_distance_at(0) > 20):
        continue
    
    fc.stop()
    meter.stop()


# turns car a specific distance
def turn_target(scanned_distances):
    mid = len(scanned_distances) // 2

    left = scanned_distances[:mid]
    right = scanned_distances[mid:]

    target = 40 # target for open space
    direction = 0 #turn direction

    if(sum(left) > sum(right)):
        direction = -1
        target = max(left)
        
    elif(sum(left) < sum(right)):
        direction = 1
        target = max(right)
    else:
        direction = 0
    
    return direction, target
        

# turns car a specified angle
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

def drive_dist(speed = 30, distance= 40, theta = 0):

    blocked = False

    trip = Duodometer(4,24)
    trip.start()
    while trip.distance < distance:

        scan_list = scanner.scan_step_dist()
        if not scan_list:
            continue
        scan_list = [200 if d < 0 else 200 if d > 200 else d for d in  scan_list] 

        ahead = scan_list[2:8]

        if min(ahead) > 35:
            if  blocked:
                trip.start()
                blocked = False
                
            fc.forward(speed)
            continue
        elif min(scan_list) > 20:
            fc.forward(5)
            continue


        fc.stop()

        left = scan_list[:5]
        right = scan_list[5:]

        # -1 = turn left, 0 forward, 1 turn right
        direction = 0
        target = 40
        print(left, right)
        if(sum(left) > sum(right)):
            direction = -1
            target = max(left) / 2
        elif(sum(left) < sum(right)):
            direction = 1
            target = max(right) /2
        else:
            direction = 0

        
        # don't track turns
        if not blocked:
            blocked = True
            trip.stop()
        
        print(target)
        if direction  == -1:
            print("turning left")
            turn_track.reset()
            while(fc.get_distance_at(0) < target):
                fc.turn_left(10)
            theta += gps.dist_to_angle(turn_track.distance)

        elif direction  == 1:
            print("turning right")
            turn_track.reset()
            while(fc.get_distance_at(0) < target):
                fc.turn_right(10)
            theta -= gps.dist_to_angle(turn_track.distance)

        else:
            while(fc.get_distance_at(0) < 40):
                fc.backward(2)

    fc.stop()
    trip.stop()
    print(theta, trip.distance)

    turn_track.stop()
    return theta, trip.distance