import time, math
import picar_4wd as fc

import sys
import time

import scanner
from car import Car
from odometer import Duodometer



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


def drive_basic():
    picar = Car()

    picar.turn_right(90)
    picar.turn_left(90)
    picar.forward(10)
    picar.backward(10)




def drive_target(start:tuple, target:tuple):

    car_theta = 0
    curr_distance = 0
    nav = GPS(map_width = 50, map_length = 50, resolution = 5, start_x = 25, start_y = 0)

    instructions = nag.set_navigation_goal(target)

    # while not at target
    while(len(instructions) > 0):
        continue

    
    



if __name__ == "__main__":
    try: 
        drive_basic()

    finally: 
        fc.get_distance_at(0)
        fc.stop()
