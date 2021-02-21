


import odometer
import gps


class Car(object):
    """
    A Singleton class for the cars functions representing
    the picar itself
    """
    
    # should ideally be a singleton class
    def __init__(self, power: int = 10):

        self.power = power

        # initialize odometers

        # tracks the entire trip
        self.trip_meter = Duodometer(4, 24)

        # used for single moves
        self.move_meter = Duodometer(12, 22)
        
    
    def turn_right(self, power = 5, angle):
        dist = angle_to_dist(angle)


        move_meter.start()
        
        fc.turn_right(power)
        while(move_meter.distance < dist):
            continue
        
        fc.stop()
        move_meter.stop()
        move_meter.reset()
        

    def turn_left(self, power = 5, angle):
        dist = angle_to_dist(angle)
        move_meter.start()
        fc.turn_left(power)
        while(move_meter.distance < dist):
            continue
        
        fc.stop()
        move_meter.stop()
        move_meter.reset()

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