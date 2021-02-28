
import threading
from queue import Queue
import time
import picar_4wd as fc



def move(q):
    fc.forward(1)
    while True:
        x = q.get()
        if x != None:
            print("blocked", x)
            fc.stop()
            time.sleep(1)
            print("moving on")
            fc.forward(1)
            
        obstacles.task_done()

def stopper(q):
    time.sleep(1)
    for i in range(10):
        q.put(i)
        time.sleep(3)


if __name__ == "__main__":
    try:
        obstacles = Queue()
        threading.Thread(target=move, args=(obstacles,), daemon=True).start()
        stopper(obstacles)
        obstacles.join()
    finally:
        fc.stop()