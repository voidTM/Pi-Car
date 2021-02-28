
import threading
import queue
import time
import picar_4wd as fc

obstacles = queue.Queue()


def move():
    fc.forward(1)
    while True:
        x = obstacles.get()
        if x != None:
            print("blocked", x)
            fc.stop()
            time.sleep(1)
            print("moving on")
            fc.forward(1)
            
        obstacles.task_done()

def stopper():
    time.sleep(1)
    for i in range(10):
        obstacles.put(i)
        time.sleep(3)


if __name__ == "__main__":
    try:
        threading.Thread(target=move, daemon=True).start()
        stopper()
        obstacles.join()
    finally:
        fc.stop()