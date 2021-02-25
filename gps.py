
import time, math

import sys
import numpy as np

import utils
from queue import PriorityQueue
from collections import deque


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
        self.f_grid = np.zeros([map_width,map_length])
        self.grid_size = [map_width, map_length]
        self.resolution = resolution
        self.pos_x = start_x
        self.pos_y = start_y
        self.target_x = None
        self.target_y = None

    # loads a grid
    def load_grid(self, grid: np.array, resolution: int = 5, start_x: int = None, start_y: int = None):
        self.grid = grid
        self.resolution = resolution
        self.grid_size = [len(grid), len(grid[0])]
        self.h_grid = np.array(grid)
        self.f_grid = np.array(grid)

        if start_x is None:
            self.pos_x = len(grid) // 2
        else:
            self.pos_x = start_x
        if start_x is None:
            self.pos_y = len(grid[0]) // 2
        else: 
            self.pos_y = start_y

        self.target_x = None
        self.target_y = None

    def save_grid(self, filepath: str = 'maps/testmap.out'):
        np.savetxt(filepath, self.grid, fmt='%i', delimiter=',')

    @property
    def position(self):
        return (self.pos_x, self.pos_y)

    # check to see if a coordinate is in map bounds
    def in_bounds(self, x: int, y: int):
        
        if x < 0 or x >= self.grid_size[0]:
            return False 
        if y < 0 or y >= self.grid_size[1]:
            return False
        
        return True

    #sets a new position for the car    
    def set_postion(self, new_x: int, new_y : int):
        self.pos_x = new_x
        self.pos_y = new_y
    

    # calculate distance driven from previous point
    def update_postion(self, distance, orientation):
        x_dist, y_dist = utils.pol2cart(orientation, distance)
        
        self.pos_x += (x_dist // self.resolution)
        self.pos_y += (y_dist // self.resolution)


    # takes in an obstacles polar coordinates from car
    def add_relative_obstacle(self, orientation, distance):
        
        # add in cars orientation
        obs_x, obs_y = utils.pol2cart(orientation, distance)

        obs_x = (obs_x // self.resolution) + self.pos_x
        obs_y = (obs_y // self.resolution) + self.pos_y
        self.add_obstacle(int(obs_x), int(obs_y))

    def add_obstacle(self, obstacle_x, obstacle_y):
        
        # look for nearby obstacles
        self.obstacles.append([obstacle_x, obstacle_y])

        if self.in_bounds(obstacle_x, obstacle_y):
            # link with other nearby obstacles
            # add to grid
            print("in bounds")
            self.grid[obstacle_x][obstacle_y] = 1
        else:
            print("out of bounds", obstacle_x, obstacle_y)




    # astar navigation
    # sets a new target

    def set_navigation_goal(self, goal: tuple):
        start = (self.pos_x, self.pos_y)
        path = self.astar(start, goal)
        instructions = self.path_to_instruction(path)
        return instructions
    
    # trunctates a list of points into a path
    def path_to_instruction(self, path):
        
        # maps direction to instruction
        
        # car orientation
        direction_map = {(0,1): 0, (-1,0): 90, (0, -1): 180, (1,0):270}

        prev = path.popleft()
        prev_direction = None

        # use dequeue instead?
        instructions = deque()

        while len(path) > 0:
            curr = path.popleft()

            dx = curr[0] - prev[0]
            dy = curr[1] - prev[1]

            # get new direction
            new_direction = direction_map[(dx, dy)]


            
            if prev_direction == new_direction:
                prev_instruction = instructions.pop()
                merge = (prev_direction, prev_instruction[1] + self.resolution)
                instructions.append(merge)
                #instructions[-1] = merge
            else:
                instructions.append((prev_direction, self.resolution))
            

            prev = curr

            prev_direction = new_direction

        print(instructions)
        return instructions
 


    # reconstructs the path 
    def reconstructPath(self, cameFrom, goal):
        # stack style
        path = deque()
        node = goal
        path.appendleft(node)

        while node in cameFrom:
            node = cameFrom[node]
            path.appendleft(node)
        np.savetxt("maps/solution.out", self.f_grid, fmt='%i', delimiter=',')

        return path

    def distBetween(self,current, neighbor):
        # since only straights
        return 10

    def heuristicEstimate(self,start,goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


    # same goal but need new path
    def recalculate_navigation(self):
        pass

    def find_neighbors(self, curr_p):
        neighbors = []

        neighbors.append([curr_p[0] + 1, curr_p[1]]) #right
        neighbors.append([curr_p[0] - 1, curr_p[1]]) #left

        neighbors.append([curr_p[0], curr_p[1] + 1]) # above
        neighbors.append([curr_p[0], curr_p[1] - 1]) # below

        for neighbor in neighbors:
            if self.in_bounds(neighbor[0], neighbor[1]): # in bounds
                if self.grid[neighbor[0]][neighbor[1]] != 1: # not an obstacle
                    yield tuple(neighbor)


    # coordinates need to be stored and recieved as tuples
    def astar(self, start: tuple, goal: tuple):

        # path/dict of path and objects
        cameFrom = {} # likely store this as part of the class?

        openNodes = PriorityQueue()
        openNodes.put((0, start))
        gScore = {}
        fScore = {}

        gScore[start] = 0
        fScore[start] = gScore[start] + self.heuristicEstimate(start,goal)

        while not openNodes.empty():
            curr_score, curr_pos = openNodes.get() # priority queue should pop the lowest
            if curr_pos == goal:
                return self.reconstructPath(cameFrom, goal)
            

            for neighbor in self.find_neighbors(curr_pos):
                # since no diagonals just use a flat number?
                tentative_gScore = gScore[curr_pos] + self.distBetween(curr_pos, neighbor)

                # already been calculated before and score is higher
                if neighbor not in gScore or tentative_gScore < gScore[tuple(neighbor)]:
                    # adds to current set if not in
                    cameFrom[neighbor] = curr_pos
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self.heuristicEstimate(neighbor,goal)
                    self.f_grid[neighbor[0]][neighbor[1]] = fScore[neighbor]
                    openNodes.put((fScore[neighbor] ,neighbor))



