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
    #time.sleep(1)
    for i in range(10):
        obstacles.put(i)
        time.sleep(10)


def obstacle_ahead():
    x = obstacles.get()
    return x


def drive():
    speed = 2
    scan_dist = 35
    
    blocked = False

    fc.forward(speed)

    while True:
        
        scan_list = fc.scan_step(scan_dist)
        if not obstacles.empty():
            x = obstacles.get()
            print("blocked", x)
            fc.stop()
            time.sleep(1)
            print("moving on")
            obstacles.task_done()

        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2,2,2,2]:
            scan_dist = 50
            
            fc.turn_right(speed)
        else:
            scan_dist = 20
            fc.forward(speed)
        


if __name__ == "__main__":
    try: 
        threading.Thread(target=stopper, daemon=True).start()
        drive()
        obstacles.join()
    finally: 
        fc.get_distance_at(0)
        fc.stop()
