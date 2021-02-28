
import numpy as np
import matplotlib.pyplot as plt
import sys
from PIL import Image


import time, math
import picar_4wd as fc

import utils
from odometer import Duodometer
import gps
from car import Car

# test cases

x = [ 31,  31,  32,  34,  36,  38,  32,  37,  42,  50,  58,  75,  99, 113, 125, 134, 141, 146, 149]
y = [ 0,  3,  6,  9, 12, 15, 32, 36, 46, 48, 48, 70, 86, 75, 63, 48, 33, 16,  0]

x1 = [-15, -14, -11,  -6,   0,  51,  11,  24,  39,  50,  61,  61,  66,
        71,  74,  78,  81,  85,  48]
y1 = [ 0, 11, 22, 32, 42, -1, 68, 73, 65, 65, 64, 31, 28, 25, 20, 16, 11,
        6,  0]

x2 = [-15, -14, -10,  -6,   0,   7,  11,  24,  37,  50,  61,  61,  66,
        71,  74,  78,  81,  86,  48]
y2 = [ 0, 11, 22, 32, 42, 51, 68, 73, 76, 66, 64, 32, 28, 25, 20, 16, 11,
        6,  0]


x3 = [-18, -60, -19, -16, -14, -11,  -9,  -6,  -3,   0,  13,  11,  16,
        20,  25,  30,  -1,  -1,  66]
y3 = [ 0, 10,  7,  9, 11, 14, 15, 17, 19, 78, 77, 32, 28, 24, 21, 17,  0,
        0,  0]

x4 = [-20, -20, -19, -17, -15, -13, -11,  -8,  -4,   0,   4,   7,  10,
        13,  16,  19,  22,  -1,  -2]
y4 = [ 0,  3,  7, 10, 12, 16, 20, 24, 24, 24, 25, 20, 18, 16, 13, 11,  8,
        0,  0]


dist_hash = {-60: 43.81, -55: 39.73, -50: 28.51, -45: 16.66, -40: 45.28, -35: 31.53, -30: 29.36, -25: 28.94, -20: 29.02, -15: 28.58, -10: 29.01, -5: 29.83, 0: 30.54, 5: 39.72, 10: 40.88, 15: 38.71, 20: 39.19, 25: 38.93, 30: 37.94, 35: 39.42, 40: 43.75, 45: 44.21, 50: 44.08, 55: 43.55, 60: 39.67}


def move_test():

    picar = Car()
    print("turning left")
    picar.turn_left(90)
    time.sleep(1)
    print("turning right")
    picar.turn_right(90)
    time.sleep(1)
    print("driving forward")
    picar.drive_forward(20)
    time.sleep(1)
    print("driving backward")
    picar.drive_backward(20)

if __name__ == "__main__":
    try: 
        move_test()
        

    finally: 
        fc.stop()
        fc.get_distance_at(0)
