from picar_4wd.speed import Speed
import RPi.GPIO as GPIO
import time, math
import threading
import picar_4wd as fc

import sys
import tty
import termios
import asyncio
import time


def forward(speed):
    no_obstacle = True
    fc.forward(speed)
    while no_obstacle:
        scan_stat = fc.get_status_at(0)

        if scan_stat < 1:
            no_obstacle = False


def backup(speed):
    # time.sleep(2)
    fc.backward(speed)
    for i in range(10):
        time.sleep(0.1)
    fc.stop()

# find new direction
def turn(speed):
    fc.turn_right(speed)

if __name__ == "__main__":
    try: 
        forward(10)
        backup(10)
        turn(10)
    finally: 
        fc.get_distance_at(0)
        fc.stop()
