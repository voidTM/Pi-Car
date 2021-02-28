import time, math
import threading, queue

import picar_4wd as fc

import sys
import tty
import termios
import asyncio
import time

import detect_picamera as picam

q = queue.Queue()

def drive(obstacles: queue.Queue):
#def drive():
    speed = 2
    scan_dist = 20
    
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
        #threading.Thread(target=picam.main_camera,args=(q,), daemon=True).start()
        #threading.Thread(target=stopper, args=(obstacles,), daemon=True).start()
        drive(q)
    finally: 
        q.join()
        fc.get_distance_at(0)
        fc.stop()
