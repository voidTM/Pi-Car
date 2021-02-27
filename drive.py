import time, math
import picar_4wd as fc

import sys
import time
from collections import deque

import scanner
import utils
from car import Car
from odometer import Duodometer
from gps import GPS



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



# drives toward a certain target
def drive_target(target:tuple):

    car_theta = 0
    curr_distance = 0
    nav = GPS(map_width = 20, map_length = 20, resolution = 10, start_x = 10, start_y = 0)
    picar = Car()
    instructions = nav.set_navigation_goal(target)
    i = 0
    print("iteration:", i)
    print(instructions)

    # while not at target
    while(len(instructions) > 0):
        # convert instructions to polar
        step = instructions.popleft()
        print("directions: ", step)
        direction = step[0] - picar.orientation
        
        driven = 0
        # change direction if needed
        if direction > 0:
            picar.turn_right(direction)
        elif direction < 0:
            picar.turn_left(abs(direction))

        if step[1] >= 0:
            driven = picar.drive_forward(distance = step[1])
        else:
            driven = picar.drive_backward(distance = abs(step[1]))

        nav.update_postion(distance = int(driven), orientation = picar.orientation)
        print( "nav position", nav.position)

        # if blocked rerout
        if driven < step[1]:
            i += 1
            print("blocked!, rerouting")
            #print(int(driven), step[1])
            # scan for obstacles
            obstacles = scanner.mapping_scan()
            print(obstacles)
            # add obstacles
            for obst in obstacles:
                #print(obst)
                abs_orient = obst[0] + picar.orientation
                nav.add_relative_obstacle(orientation = abs_orient, distance = obst[1])
            
            print("iteration:", i)

            # reroute
            instructions = nav.set_navigation_goal(target)
            #print(instructions)


def drive_instructions(picar: Car, nav:GPS, instructions:deque):

    while(len(instructions) > 0):
        # convert instructions to polar
        step = instructions.popleft()
        print("directions: ", step)
        direction = step[0] - picar.orientation
        
        driven = 0
        # change direction if needed
        if direction > 0:
            picar.turn_right(direction)
        elif direction < 0:
            picar.turn_left(abs(direction))

        if step[1] >= 0:
            driven = picar.drive_forward(distance = step[1])
        else:
            driven = picar.drive_backward(distance = abs(step[1]))

        nav.update_postion(distance = int(driven), orientation = picar.orientation)
        print( "nav position", nav.position)

        # if blocked rerout
        if driven < step[1]:
            i += 1
            print("blocked!")
            print("remaining instructions:", instructions)
            
            return

def turn_test():

    picar = Car()
    for i in range(0,10):
        picar.turn_left(90)
        time.sleep(1)
        picar.turn_right(90)
        time.sleep(1)

    
if __name__ == "__main__":
    try: 
        #drive_target((0, 10))
        turn_test()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
