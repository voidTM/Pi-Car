
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
    def __init__(self, map_size: int = 200, resolution: int = 5, start_x: int = 100, start_y: int 100):

        self.grid = np.full((200, 200), 0, dtype = int)
        self.resolution = resolution
        self.pos_x = start_x
        self.pos_y = start_y
        self.target_x = None
        self.target_y = None

    # loads a grid
    def load_grid(self, grid: np.array, resolution: int = 5, start_x: int = None, start_y: int = None):
        self.grid = grid
        self.resolution = resolution
        self.orientation = orientation

        if start_x is None:
            self.pos_x = len(grid) // 2
        if start_x is None:
            self.pos_y = len(grid[0]) // 2

        self.target_x = None
        self.target_y = None


    #sets a new position for the car    
    def set_postion(self, new_x, new_y):
        self.pos_x = new_x
        self.pos_y = new_y
    

    # calculate distance driven from previous point
    def update_postion(self, distance, orientation):
        x_dist, y_dist = utils.pol2cart(orientation, distance)
        
        self.pos_x += x_dist
        self.pos_y += y_dist


    def set_target(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

    def add_relative_obstacle(self, obstacle_direction, obstacle_angle):
    def add_obstacle(self, obstacle_x, obstacle_y):
