
import time, math

import sys
import time


import numpy as np



# goal is to track the car's position on a map

class GPS(object):
    """
    Keeps track of a cars position and orientation on a grid/map
    """
    goal = None
    # list of obstacles
    obstacles = []


    # starts with an empty grid
    def __init__(self, map_width: int = 200, map_length: int = 200, resolution: int = 5, start_x: int = 100, start_y: int = 100):

        self.grid = np.full((map_width, map_length), 0, dtype = int)
        
        # weighted grid fro nump
        self.h_grid = np.zeros([map_width,map_length])

        self.grid_size = [200, 200]
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
        self.grid_size = [len(grid), len(grid[0])]

        if start_x is None:
            self.pos_x = len(grid) // 2
        if start_x is None:
            self.pos_y = len(grid[0]) // 2

        self.target_x = None
        self.target_y = None

    def save_grid(self, filepath: str = 'maps/testmap.out'):
        np.savetxt(filepath, self.grid, fmt='%i', delimiter=',')


    # check to see if a coordinate is in map bounds
    def in_map_bounds(self, x: int, y: int):

        if x < 0 or x > self.grid_size[0]:
            return False 
        if y < 0 or y > self.grid_size[1]:
            return False
        
        return True

    #sets a new position for the car    
    def set_postion(self, new_x: int, new_y : int):
        self.pos_x = new_x
        self.pos_y = new_y
    

    # calculate distance driven from previous point
    def update_postion(self, distance, orientation):
        x_dist, y_dist = utils.pol2cart(orientation, distance)
        
        self.pos_x += x_dist
        self.pos_y += y_dist


    # takes in an obstacles polar coordinates from car
    def add_relative_obstacle(self, obstacle_direction, obstacle_angle):
        
        obs_x, obs_y = utils.pol2cart(orientation, distance)

        obs_x += self.pos_x
        obs_y += self.pos_y
        add_obstacle(obs_x, obs_y)

    def add_obstacle(self, obstacle_x, obstacle_y):
        
        # look for nearby obstacles
        obstacles.append([obstacle_x, obstacle_y])

        if self.in_map_bounds(obstacle_x, obstacle_y):
            # link with other nearby obstacles
            # add to grid
            self.grid[obstacle_x][obstacle_y] = 1


    # astar navigation
    # sets a new target
    def set_navigation_goal(self, goal):

        current = [self.pos_x, self.pos_y]
        cameFrom = {}
        openSet = set([current])
        closedSet = set()


        gScore = {}
        fScore = {}
        gScore[start] = 0
        fScore[start] = gScore[start] + self.heuristicEstimate(start,goal)
        while len(openSet) != 0:
            current = self.getLowest(openSet,fScore)
            if current == goal:
                return self.reconstructPath(cameFrom,goal)
            openSet.remove(current)
            closedSet.add(current)
            for neighbor in self.neighborNodes(current):
                tentative_gScore = gScore[current] + self.distBetween(current,neighbor)
                if neighbor in closedSet and tentative_gScore >= gScore[neighbor]:
                    continue
                if neighbor not in closedSet or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self.heuristicEstimate(neighbor,goal)
                    if neighbor not in openSet:
                        openSet.add(neighbor)
        return 0

    # same goal but need new path
    def recalculate_navigation(self):
        pass