
import time, math
import picar_4wd as fc

import utils
import odometer
import gps


class Car(object):
    """
    A Singleton class for the cars functions representing
    the picar itself
    """
    
    orientation = 0

    # should ideally be a singleton class
    def __init__(self, power: int = 10):

        self.power = power

        # initialize odometers

        # tracks the entire trip
        self.trip_meter = Duodometer(4, 24)

        # used for single moves
        self.move_meter = Duodometer(12, 22)
        
        
    # turning
    def turn(angle, power = 10):
        turn_dist = gps.angle_to_dist(angle)

        if angle < 0:
            self.turn_left(abs)
        elif angle > 1:
            while(fc.get_distance_at(0) < turn_dist):
                fc.turn_right(power)
        else:
            while(fc.get_distance_at(0) < turn_dist):
                fc.backward(2)

    def turn_right(self, power = 5, angle):
        dist = angle_to_dist(angle)


        move_meter.start()
        
        fc.turn_right(power)
        while(move_meter.distance < dist):
            continue
        
        fc.stop()
        move_meter.stop()
        move_meter.reset()
        
    def turn_right_dist(self, power)

    # basic car drive functionality
    def turn_left(self, power = 5, angle):
        dist = angle_to_dist(angle)
        move_meter.start()
        fc.turn_left(power)
        while(move_meter.distance < dist):
            continue
        
        fc.stop()
        move_meter.stop()
        move_meter.reset()

        # update 
        
    
    def drive_forward(self, power = 5, distance = 10):

        move_meter.start()
        fc.forward(power)
        while(move_meter.distance < dist and fc.get_distance_at(0) > 20):
            continue
        
        fc.stop()
        actually_traveled = move_meter.distance
        move_meter.stop()
        move_meter.reset()

        return actually_traveled
    
    def drive_backward(self, power = 5, distance = 10)
        move_meter.start()
        fc.drive_backward(power)

        while(move_meter.distance < dist):
            continue
        
        fc.stop()
        actually_traveled = move_meter.distance
        move_meter.stop()
        move_meter.reset()

        return distance




# turns towards its target

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
