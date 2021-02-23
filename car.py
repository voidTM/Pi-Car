
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
        
        
    # turning
    def turn(angle, power = 10):

        if angle < 0:
            self.turn_left(angle)
        elif angle > 1:
            self.turn_right(angle)
        else:
            while(fc.get_distance_at(0) < turn_dist):
                fc.backward(2)

    # right turns
    def turn_right(self, power = 5, angle):
        dist = utils.angle_to_dist(angle)


        self.trip_meter.reset()        
        fc.turn_right(power)
        while(self.trip_meter.distance < dist):
            continue
        
        fc.stop()

        orientation -= angle

        return orientation
        
    def turn_right_target(self, power = 5, target):

        self.trip_meter.start()
        fc.turn_right(power)
        while(fc.get_distance_at(0) < target):
            continue
        fc.stop()
        self.trip_meter.stop()

        distance_turned = self.trip_meter.distance
        # netagive angle for right turn
        angle = dist_to_angle(distance_turned)

        orientation -= angle

        return orientation


    # left turns
    def turn_left(self, power = 5, angle):
        dist = utils.angle_to_dist(angle)
        self.trip_meter.reset()

        fc.turn_left(power)
        while(self.trip_meter.distance < dist):
            continue
        
        fc.stop()

        # update 
        orientation += angle

        return orientation
    
    def turn_left_target(self, power = 5, target):

        self.trip_meter.reset()
        fc.turn_left(power)
        while(fc.get_distance_at(0) < target):
            continue
        fc.stop()

        distance_turned = self.trip_meter.distance
        # netagive angle for right turn
        angle = dist_to_angle(distance_turned)

        orientation += angle

        return orientation


    def drive_forward(self, power = 5, distance = None):

        self.trip_meter.start()
        fc.forward(power)

        # if no distance is defined then drive forward until blocked
        if distance == None:
            while(fc.get_distance_at(0) > 20):
                continue
        else:
            while(self.trip_meter.distance < dist and fc.get_distance_at(0) > 20):
                continue
        
        fc.stop()
        actually_traveled = self.trip_meter.distance
        self.trip_meter.stop()
        self.trip_meter.reset()

        return actually_traveled
    
    def drive_backward(self, power = 5, distance = 10)
        self.trip_meter.reset()
        fc.drive_backward(power)

        while(self.trip_meter.distance < dist):
            continue
        
        fc.stop()
        actually_traveled = self.trip_meter.distance

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
