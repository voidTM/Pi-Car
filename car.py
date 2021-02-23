
import time, math
import picar_4wd as fc

import utils
from odometer import Duodometer
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

        # slippage should be 2?
        self.trip_meter = Duodometer(4, 24)
        self.trip_meter.start()
        

    # right turns
    def turn_right(self, angle, power = 5):
        slippage = 1.3
        dist = utils.angle_to_dist(angle) * slippage


        self.trip_meter.reset()        
        fc.turn_right(power)
        while(self.trip_meter.distance < dist):
            continue
        
        fc.stop()

        self.orientation -= angle

        return self.orientation
        
    def turn_right_target(self, target, power = 5):

        self.trip_meter.start()
        fc.turn_right(power)
        while(fc.get_distance_at(0) < target):
            continue
        fc.stop()
        self.trip_meter.stop()

        distance_turned = self.trip_meter.distance
        # netagive angle for right turn
        angle = dist_to_angle(distance_turned)

        self.orientation -= angle

        return self.orientation


    # left turns
    def turn_left(self, angle, power = 5):
        slippage = 0.87
        dist = utils.angle_to_dist(angle) * slippage
        self.trip_meter.reset()

        fc.turn_left(power)
        while(self.trip_meter.distance < dist):
            continue
        
        fc.stop()

        # update 
        self.orientation += angle

        return self.orientation
    
    def turn_left_target(self, target, power = 5):

        self.trip_meter.reset()
        fc.turn_left(power)
        while(fc.get_distance_at(0) < target):
            continue
        fc.stop()

        distance_turned = self.trip_meter.distance
        # netagive angle for right turn
        angle = dist_to_angle(distance_turned)

        self.orientation += angle

        return self.orientation



    # turning
    def turn(self, angle, power = 10):
        print(angle)
        if angle < 0:
            self.turn_right(abs(angle))
        elif angle > 1:
            self.turn_left(angle)
        else:
            while(fc.get_distance_at(0) < turn_dist):
                fc.backward(2)

    def drive_forward(self, distance = None, power = 5):

        self.trip_meter.reset()
        fc.forward(power)

        # if no distance is defined then drive forward until blocked
        if distance == None:
            while(fc.get_distance_at(0) > 20):
                continue
        else:
            while(self.trip_meter.distance < distance and fc.get_distance_at(0) > 20):
                continue
        
        fc.stop()
        actually_traveled = self.trip_meter.distance

        return actually_traveled
    
    def drive_backward(self, distance = 10, power = 5):
        self.trip_meter.reset()
        fc.backward(power)

        while(self.trip_meter.distance < distance):
            continue
        
        fc.stop()
        actually_traveled = self.trip_meter.distance

        return actually_traveled




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
