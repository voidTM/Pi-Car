
import time, math

import sys
import time


import numpy as np



# goal is to track the car's position on a map

class GPS(object):
    """
    Keeps track of a cars position and orientation on a grid/map
    """
    destination = None
    pathing = False

    # starts with an empty grid
    def __init__(self, map_size: int = 200, resolution: int = 5, start_x: int = 100, start_y: int 100, orientation: int = 0):

        self.grid = np.full((200, 200), 0, dtype = int)
        self.resolution = resolution
        self.orientation = orientation
        self.pos_x = start_x
        self.pos_y = start_y


    # loads a grid
    def load_grid(self, grid: np.array, resolution: int = 5, start_x: int = None, start_y: int = None, orientation: int = 0):
        self.grid = grid
        self.resolution = resolution
        self.orientation = orientation

        if start_x is None:
            self.pos_x = len(grid) // 2
        if start_x is None:
            self.pos_y = len(grid[0]) // 2

    
    def update_pos(self, new_x, new_y):
        self.pos_x = new_x
        self.pos_y = new_y
    
    def update_orientation(self, new_theta):
        self.orientation = new_theta