
import time, math
import picar_4wd as fc

import utils
from odometer import Duodometer
import gps

import scanner
import detect

class Car(object):
    """
    A Singleton class for the cars functions representing
    the picar itself
    """
    

    # should ideally be a singleton class
    def __init__(self):


        # initialize odometers
        self.orientation = 0
        # slippage should be 2?
        self.trip_meter = Duodometer(4, 25)
        self.trip_meter.start()
        

    # right turns
    def turn_right(self, angle: int, power: int = 5):
        # need to adjust slippage for turning
        slippage = 2.1
        dist = utils.angle_to_dist(angle) * slippage


        self.trip_meter.reset()        
        fc.turn_right(power)
        while(self.trip_meter.distance < dist):
            continue
        
        fc.stop()

        self.orientation = update_angle(self.orientation, angle)
        print("new car orientation", self.orientation)

        return self.orientation
        
    def turn_right_target(self, target: float, power: int = 5):
        slippage = 2.1
        self.trip_meter.start()
        fc.turn_right(power)
        while(fc.get_distance_at(0) < target):
            continue
        fc.stop()
        self.trip_meter.stop()

        distance_turned = self.trip_meter.distance * 0.65
        # netagive angle for right turn
        angle = dist_to_angle(distance_turned)

        self.orientation = update_angle(self.orientation, angle)
        print("angle turned", angle)
        print("new car orientation", self.orientation)

        return self.orientation


    # left turns
    def turn_left(self, angle: int, power: int = 5):
        # need to adjust slippage for turning

        slippage = 1.95 #1.74
        #siippage = 1.95
        dist = utils.angle_to_dist(angle) * slippage
        self.trip_meter.reset()

        fc.turn_left(power)
        while(self.trip_meter.distance < dist):
            continue
        
        fc.stop()

        # update 
        self.orientation = update_angle(self.orientation, -angle)
        print("new car orientation", self.orientation)

        return self.orientation
    
    def turn_left_target(self, target: float, power: int = 5):
        # need to adjust slippage for turning
        slippage = 2

        self.trip_meter.reset()
        fc.turn_left(power)
        while(fc.get_distance_at(0) < target):
            continue
        fc.stop()

        distance_turned = self.trip_meter.distance
        # netagive angle for right turn
        angle = dist_to_angle(distance_turned)

        self.orientation = update_angle(self.orientation, -angle)
        print("new car orientation", self.orientation)

        return self.orientation



    # turning
    def turn(self, angle: int, power: int = 10):
        print(angle)
        if angle < 0:
            self.turn_right(abs(angle))
        elif angle > 1:
            self.turn_left(angle)
        else:
            while(fc.get_distance_at(0) < turn_dist):
                fc.backward(2)

    def drive_forward(self, distance: int = None, power: int = 5):

        self.trip_meter.reset()
        fc.forward(power)
        coast_clear = True
        # if no distance is defined then drive forward until blocked
        if distance == None:
            while(coast_clear):
                continue
        else:
            while(self.trip_meter.distance < distance and coast_clear):
                if (fc.get_status_at(0, 20) != 2):
                    coast_clear = False
                continue
        
        fc.stop()
        print(self.trip_meter.distance, distance)

        actually_traveled = self.trip_meter.distance

        return actually_traveled
    
    def drive_forward2(self, distance: int, obstacles: power: int = 5):
        self.trip_meter.reset()
        fc.forward(power)
        clear = True
        while(self.trip_meter.distance < distance):
            scan_list = fc.scan_step(20)
            if not scan_list:
                continue
            tmp = scan_list[3:7]
            if tmp != [2,2,2,2]:
                blocked = True
                break
        fc.stop()
        if blocked:
            self.drive_backward(10)
                    

    def drive_backward(self, distance = 10, power = 5):
        self.trip_meter.reset()
        fc.backward(power)

        while(self.trip_meter.distance < distance):
            continue
        
        fc.stop()
        actually_traveled = self.trip_meter.distance

        return actually_traveled




def update_angle(angle1:int, angle2:int):
    return (angle1 + angle2 + 360) %360
    

# the car class with picam model dection added
class CamCar(Car):

    def __init__(self, model:str , label:str ):
        super().__init__(self)

