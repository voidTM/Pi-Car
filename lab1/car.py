
import time, math
import picar_4wd as fc


from queue import Queue
from collections import deque
from threading import Thread

from odometer import Duodometer
from gps import GPS
import gps, scanner, utils
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
        slippage = 2.2 
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
        slippage = 2.2
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

        slippage = 2.05 #1.74
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

    def drive_forward(self, distance: int, power: int = 5):

        self.trip_meter.reset()
        fc.forward(power)
        coast_clear = True
        while(self.trip_meter.distance < distance and coast_clear):
            if (fc.get_status_at(0, 20) != 2):
                coast_clear = False
                break
            continue
        
        fc.stop()
        print(self.trip_meter.distance, distance)



        return coast_clear
    

    def drive_backward(self, distance = 10, power = 5):
        self.trip_meter.reset()
        fc.backward(power)

        while(self.trip_meter.distance < distance):
            continue
        
        fc.stop()

        actually_traveled = self.trip_meter.distance

        return actually_traveled

    def handle_obstacle(self, obstacle: tuple):
        pass


class PiCar(Car):

    def __init__(self, nav: GPS):
        super().__init__()
        self.nav = nav
        self.obstacle_queue = Queue()
        self.shutoff = False
        self.cam = Thread(target=detect.look_for_objects,args=(self.shutoff, self.obstacle_queue,), daemon=True)
        self.cam.start()

    def drive_forward_cam(self, distance: int, power: int = 2):
        self.trip_meter.reset()
        fc.forward(power)
        coast_clear = True

        # clear obstacles 
        with self.obstacle_queue.mutex:
            self.obstacle_queue.queue.clear()
        
        while(self.trip_meter.distance < distance and coast_clear):

            # handle obstacles
            if not self.obstacle_queue.empty():
                fc.stop()

                print(self.obstacle_queue.qsize())
                o = self.obstacle_queue.get()

                if o == "obstacle":
                    coast_clear = False                    
                    break
                else: # must stop
                    self.obstacle_queue.task_done()
                    with self.obstacle_queue.mutex:
                        self.obstacle_queue.queue.clear()
                    time.sleep(1)
                    
            else:
                fc.forward(power)

        # switch to something else?
        with self.obstacle_queue.mutex:
            self.obstacle_queue.queue.clear()


        fc.stop()
        actually_traveled = self.trip_meter.distance

        # encountered an obstacle.
        if not coast_clear:
            self.drive_backward(15)
            actually_traveled -= 15
        
        self.nav.update_postion(actually_traveled, self.orientation)

        return coast_clear

    
        
    
    # drives towards a target
    def drive_target(self, target: tuple):
        
        at_destination = False

        while(not at_destination):

            # scan for obstacles
            obstacles = scanner.mapping_scan()
            #print("Scan results")
            #print(obstacles)
            #print(" ")

            # resets the grid for more up to date results.
            self.nav.clear_grid()

            # adds in new obstacles
            for obst in obstacles:
                abs_orient = obst[0] + self.orientation
                self.nav.add_relative_obstacle(orientation = abs_orient, distance = obst[1])
                
            instructions = self.nav.set_navigation_goal(target)
            
            at_destination = self.drive_instructions(instructions)

        print("arrived at destination")

    # drive according to instructions until blocked or finished
    def drive_instructions(self, instructions:deque):

        # while not at target
        steps_taken = 0
        while(len(instructions) > 0):
            # convert instructions to polar
            step = instructions.popleft()
            print("directions: ", step)
                    
            # calculate the shortest angle to turn
            direction = step[0] - self.orientation
            direction = (direction + 180) % 360 - 180
            #print("turning angle", direction)

            
            # change direction if needed
            if direction > 0: 
                self.turn_right(direction)
            elif direction < 0:
                self.turn_left(abs(direction))

            
            coast_clear = self.drive_forward_cam(distance = step[1])

            steps_taken += 1

            # need to recalibrate
            if not coast_clear or steps_taken == 3:
                return False

    
        return True

    
    
    
    def __del__(self):
        self.shutoff = True
        self.cam.join(2)
        with self.obstacle_queue.mutex:
            self.obstacle_queue.queue.clear()
        self.obstacle_queue.join()

    

# updates and normalizes the angle to be within 0-360
def update_angle(angle1:int, angle2:int):
    return (angle1 + angle2 + 360) %360
