
from picar_4wd.speed import Speed
import time, math
import threading
import picar_4wd as fc
import numpy as np


ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
MAX_ANGLE = ANGLE_RANGE//2
MIN_ANGLE = -ANGLE_RANGE//2

scan_status = []
scan_dist = []

# holds all the scanning info

def next_step():
    global current_angle, us_step, MAX_ANGLE, MIN_ANGLE
    current_angle += us_step
    if current_angle >= MAX_ANGLE:
        current_angle = MAX_ANGLE
        us_step = -STEP
    elif current_angle <= MIN_ANGLE:
        current_angle = MIN_ANGLE
        us_step = STEP
    return current_angle

def scan_step_status(ref1 , ref2):
    global scan_status, current_angle, us_step

    current_angle += us_step
    if current_angle >= MAX_ANGLE:
        current_angle = MAX_ANGLE
        us_step = -STEP
    elif current_angle <= MIN_ANGLE:
        current_angle = MIN_ANGLE
        us_step = STEP

    status = get_status_at(current_angle, ref1=ref1, ref2=ref2)#ref1

    scan_status.append(status)
    if current_angle == MIN_ANGLE or current_angle == MAX_ANGLE:
        if us_step < 0:
            # print("reverse")
            scan_list_status.reverse()
        # print(scan_list)
        tmp = scan_list_status.copy()
        scan_list_status = []
        return tmp
    else:
        return False

def scan_step_dist():
    global scan_dist, current_angle, us_step
    current_angle += us_step
    if current_angle >= MAX_ANGLE:
        current_angle = MAX_ANGLE
        us_step = -STEP
    elif current_angle <= MIN_ANGLE:
        current_angle = MIN_ANGLE
        us_step = STEP

    dist = fc.get_distance_at(current_angle)

    scan_dist.append(dist)
    if current_angle == MIN_ANGLE or current_angle == MAX_ANGLE:
        if us_step < 0:
            # print("reverse")
            scan_dist.reverse()
        # print(scan_list)
        tmp = scan_dist.copy()
        scan_dist = []
        return tmp
    else:
        return False


# does a full scan of the entire range
# note ultrasonic are waves and thus not entirely accurate
def mapping_scan(min_angle = MIN_ANGLE, max_angle = MAX_ANGLE, step = 5):
    # set to min_angle
    fc.get_status_at(min_angle)
    time.sleep(1)
    scan_dist = []
    for angle in range(min_angle, max_angle + 1, 5):
        # give time for settling
        time.sleep(0.1)
        scan_dist.append([angle, fc.get_distance_at(angle)])
 
    return np.array(scan_dist)


