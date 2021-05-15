# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using TF Lite to detect objects with the Raspberry Pi camera."""

import detect
from threading import Thread
from queue import Queue

ender = False
def handle_obstacles(obstacles:Queue):

    while True:
        if obstacles.empty():
            continue
        
        o = obstacles.get()
        print(o)
        obstacles.task_done()

def multithread_cam():
    try:
        obstacles = Queue()
        x = Thread(target=detect.look_for_objects,args=(ender, obstacles,), daemon=True)
        x.start()
        handle_obstacles(obstacles)
    finally:
        ender = True
        obstacles.join()
        x.join(2)



def loop_cam(shutoff: bool):  

    traffic = detect.TrafficCam(fast = True)

    while(shutoff == False):
        print(traffic.detect_traffic())


if __name__ == '__main__':
    # multithread_cam()
    loop_cam(False )
