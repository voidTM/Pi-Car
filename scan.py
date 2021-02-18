
from picar_4wd.speed import Speed
import time, math
import threading
import picar_4wd as fc


ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2

scan_status = []
scan_dist = []


def next_step():
    global current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    return current_angle

def scan_step_status(ref1 , ref2):
    global scan_status, current_angle, us_step

    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP

    status = get_status_at(current_angle, ref1=ref1, ref2=ref2)#ref1

    scan_status.append(status)
    if current_angle == min_angle or current_angle == max_angle:
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
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP

    dist = fc.get_distance_at(current_angle)

    scan_dist.append(dist)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_dist.reverse()
        # print(scan_list)
        tmp = scan_dist.copy()
        scan_dist = []
        return tmp
    else:
        return False

