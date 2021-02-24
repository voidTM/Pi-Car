#!/usr/bin/python
# Created by Joao A. Jesus Jr. <joao29a@gmail.com>
#            Joao M. Velasques Faria
# modified by Sam Song


from queue import PriorityQueue
from collections import deque
import heapq
import numpy as np


class AStar:

    def distBetween(self,current,neighbor):
        # since only straights
        return 10

    def heuristicEstimate(self,start,goal):
        return abs(star[0] - goal[0]) + abs(start[1] - goal[1])


    # this should be a generator?
    def neighborNodes(self,current):
        neighbors = []
        # if not obstacle and in bounds
        return neighbors
    
    def reconstructPath(self,cameFrom,goal):
        path = deque()
        node = goal
        path.appendleft(node)
        while node in cameFrom:
            node = cameFrom[node]
            path.appendleft(node)
        return path
    # thanks to @m1sp <Jaiden Mispy> for this simpler version of
    # reconstruct_path that doesn't have duplicate entries

    def reconstruct_path(self, came_from,
                        start, goal):
        current: Location = goal
        path: List[Location] = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return path



    def getLowest(self,openSet,fScore):
        lowest = float("inf")
        lowestNode = None
        for node in openSet:
            if fScore[node] < lowest:
                lowest = fScore[node]
                lowestNode = node
        return lowestNode

    def aStar(self,start,goal):
        cameFrom = {} # likely store this as part of the class?

        openSet = set([start])
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

    def astar2(self, grid, start, goal):

        # path/dict of path and objects
        cameFrom = {} # likely store this as part of the class?

        openNodes = PriorityQueue()
        openNodes.put((0, start))
        closedNodes = set()
        gScore = {}
        fScore = {}
        hScore = {}


        while len(openSet) != 0:
            curr_w, curr_p = openNodes.get() # priority queue should pop the lowest
            if curr_p == goal:
                return self.reconstructPath(cameFrom, goal)
            
            closedNodes.put((curr_w, curr_p))

            for neighbor in self.neighborNodes(curr_p):
                # since no diagonals just use a flat number?
                tentative_gScore = gScore[current] + self.distBetween(current,neighbor)

                # already been calculated before and score is higher
                if neighbor not in closedSet or tentative_gScore < gScore[neighbor]:
                    # adds to current set if not in
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self.heuristicEstimate(neighbor,goal)
                    if neighbor not in openNodes:
                        openNodes.put((fScore[neighbor] ,neighbor))









def a_star_search(graph: np.array, start: np.array, goal: np.array):
    
    # list of 
    frontier = PriorityQueue()
    frontier.put((0, start))
    # tree 
    came_from =  Dict[Location, Optional[Location]] = {}
    cost_so_far =  Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far
