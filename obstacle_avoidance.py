import time, math
import threading, queue
import picar_4wd as fc

import sys
import tty
import termios
import asyncio
import time


obstacles = queue.Queue()

def stopper():
    time.sleep(1)
    for i in range(10):
        obstacles.put(i)
        time.sleep(4)


def obstacle_ahead():
    x = obstacles.get()
    return x


def drive():
    speed = 2
    scan_dist = 20
    
    blocked = False

    while True:
        
        if obstacle_ahead():
            fc.stop()
            time.sleep(2)
            continue

        scan_list = fc.scan_step(scan_dist)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2,2,2,2]:
            scan_dist = 50
            speed = 10
            
            fc.turn_right(speed)
        else:
            scan_dist = 20
            speed = 30
            fc.forward(speed)
        


if __name__ == "__main__":
    try: 
        drive()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
