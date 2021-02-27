import time, math
import threading
import picar_4wd as fc

import sys
import tty
import termios
import asyncio
import time

# 20 should be the minimum distance

def drive():
    speed = 2
    scan_dist = 20
    
    blocked = False

    while True:
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
            time.sleep(10)
            scan_dist = 20
            speed = 30
            fc.forward(speed)
        


if __name__ == "__main__":
    try: 
        drive()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
