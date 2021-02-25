
#from astar import AStar
import numpy as np
from gps import GPS 


def test():
    grid = np.loadtxt("maps/minimap.out", dtype = int, delimiter = ',')
    #print(grid)
    t = GPS()
    t.load_grid(grid, start_x = 0, start_y = 0)
    #t.astar(start = (0,0), goal = (17,0))
    t.set_navigation_goal((17,0))

def testempty():
    grid = np.zeros([20,20], dtype = int)

    t = GPS()
    t.load_grid(grid, start_x = 10, start_y = 0)
    instructions = t.set_navigation_goal((19, 10))

    # while not at target
    while(len(instructions) > 0):
        # convert instructions to polar
        step = instructions.pop()
        print(step)


testempty()
