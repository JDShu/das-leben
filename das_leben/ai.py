'''
* This file is part of Das Leben.
* Copyright (C) 2011 Hans Lo
*
* Das Leben is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Das Leben is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Das Leben.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import math

from direct.task import Task

NODES = (25,25) #This cannot be changed at the moment.

class AI:

    def __init__(self, game_data, character_models, objects):
        self.game_data = game_data
        self.ai_map = create_empty_map(*NODES)
        self.character_catalog = {}
        for character_id, model in character_models.items():
            self.character_catalog[character_id] = AICharacter(model, objects)
            
        taskMgr.add(self.update,"AIUpdate")

    def update(self, task):
        for character_id, ai in self.character_catalog.items():
            if ai.path:
                self.game_data.step_character(character_id, ai.path[0])
        return Task.cont

    def begin_move(self, character_id, destination):
        self.character_catalog[character_id].set_path(destination, self.ai_map)

class AICharacter:

    def __init__(self, model, objects):
        self.model = model
        self.position = int_2d_position(model.getPos())
        self.path = None
        self.moving = False

    def set_path(self, destination, ai_map):
        self.moving = True
        goal = int_2d_position(destination)
        self.path = astar_path(ai_map, self.position, goal)
        self.pop_front()
 
    def pop_front(self):
        if self.path:
            self.position = self.path[0]
            self.path = self.path[1:]


def int_2d_position(position):
    return int(math.floor(position[0])), int(math.floor(position[1]))

def get_ai_node(geo_coords):
    pass

def astar_path(map_layout, start, goal):
    g = {}
    h = {}
    f = {}
    came_from = {}
    open_set = [start]
    closed_set = set()
    g[start] = 0
    h[start] = astar_heuristic(start, goal)
    f[start] = g[start] + h[start]
    while open_set:
        expand = lowest_score_node(open_set, f)
        if expand == goal:
            return reconstruct(came_from, came_from[goal])
        open_set.remove(expand)
        closed_set.add(expand)
        neighbors = get_neighbors(expand, map_layout)
        for n in neighbors:
            if n in closed_set:
                continue
            temp_g = g[expand] + 1
            use_temp = False
            if n not in open_set:
                open_set += [n]
                use_temp = True
            elif temp_g < g[n]:
                use_temp = True

            if use_temp:
                came_from[n] = expand
                g[n] = temp_g
                h[n] = astar_heuristic(n, goal)
                f[n] = g[n] + h[n]
    raise BaseException
        
def lowest_score_node(open_set, f):
    lowest = min([(f[node],node) for node in open_set])
    return lowest[1]

def astar_heuristic(start, goal):
    return math.hypot((start[0]-goal[0]), abs(start[1]-goal[1]))

def reconstruct(came_from, current_node):
    try:
        p = reconstruct(came_from, came_from[current_node])
        return p + [current_node]
    except:
        return [current_node]

def get_neighbors(node, map_layout):
    x, y = node
    neighbors = []
    for n_x, n_y in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
        try:
            if map_layout[n_x][n_y] == 0:
                neighbors.append((n_x, n_y))
        except IndexError:
            pass
    return neighbors

def create_empty_map(w,h):
    return [[0]*w for i in range(h)]
