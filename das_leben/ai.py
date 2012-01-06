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
import sys

from direct.task import Task

import wall_layout

NODES = (25,25) #This cannot be changed at the moment.
N,S,E,W = range(4)
CELL_IN_DIRECTION = {N:(0,-1),
                     S:(0,1),
                     E:(1,0),
                     W:(-1,0)}
DIRECTION_OF_CELL = {(0,-1):N,
                     (0,1):S,
                     (1,0):E,
                     (-1,0):W}

class AI:

    def __init__(self, game_data, character_models, object_models, walls):
        self.game_data = game_data
        self.better_map = create_ai_map(object_models, walls)
        self.character_catalog = {}
        for character_id, model in character_models.items():
            self.character_catalog[character_id] = AICharacter(model, self.better_map)
        taskMgr.add(self.update,"AIUpdate")

    def update(self, task):
        for character_id, ai in self.character_catalog.items():
            if ai.current_destination:
                self.game_data.step_character(character_id, ai.current_destination)
        return Task.cont

    def begin_move(self, character_id, destination):
        new_destination = destination[0], destination[1]
        self.character_catalog[character_id].set_path(new_destination, self.better_map)

class AICharacter:

    def __init__(self, model, ai_map):
        self.model = model
        self.ai_map = ai_map
        x,y,z = model.getPos()

        self.position = x, y
        self.current_destination = None
        
        self.current_cell = ai_map.point_to_cell((x,y))
        self.next_cell = None
        
        self.path = []
        
    def set_path(self, destination, ai_map):
        goal = ai_map.point_to_cell(destination)
        if is_invalid_cell(goal):
            return
        self.final_destination = destination
        try:
            self.path = astar_path(ai_map, self.current_cell, goal, self.position)
            self.path = [(self.ai_map.cells[x][y].y_mid, self.ai_map.cells[x][y].x_mid) for x,y in self.path]
            self.path.append(destination)
            self.reached_point(self.position)
        except NoPathError:
            pass
        
    def reached_point(self, position):
        self.current_cell = self.ai_map.point_to_cell(position)
        if self.path:
            self.current_destination = self.path[0]
            self.path = self.path[1:]
        else:
            self.current_destination = None
        
    def update_path(self, model_pos):
        d_x, d_y = self.current_destination
        m_x, m_y, m_z = model_pos
        if abs(d_x - m_x) < 0.1 and abs(d_y - m_y) < 0.1:
            self.reached_point((m_x, m_y))

def astar_path(map_layout, start, goal, exact_start):
    if start == goal:
        return [start]
    g = {}
    h = {}
    f = {}
    came_from = {}
    open_set = [start]
    closed_set = set()
    g[start] = 0
    h[start] = first_astar_heuristic(exact_start, goal, map_layout)
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
            temp_g = g[expand] + distance_between(expand, n, map_layout)
            use_temp = False
            if n not in open_set:
                open_set += [n]
                use_temp = True
            elif temp_g < g[n]:
                use_temp = True

            if use_temp:
                came_from[n] = expand
                g[n] = temp_g
                h[n] = astar_heuristic(n, goal, map_layout)
                f[n] = g[n] + h[n]
    print "There is no path to", goal
    raise NoPathError(goal)
        
def lowest_score_node(open_set, f):
    lowest = min([(f[node],node) for node in open_set])
    return lowest[1]

def first_astar_heuristic(start, goal, map_layout):
    finish_cell = map_layout.cells[goal[0]][goal[1]]
    x1, y1 = start
    x2, y2 = finish_cell.x_mid, finish_cell.y_mid
    return math.hypot(x1-x2,y1-y2)
    
def astar_heuristic(start, goal, map_layout):
    return distance_between(start, goal, map_layout)

def distance_between(start, goal, map_layout):
    start_cell = map_layout.cells[start[0]][start[1]]
    finish_cell = map_layout.cells[goal[0]][goal[1]]
    x1, y1 = start_cell.x_mid, start_cell.y_mid
    x2, y2 = finish_cell.x_mid, finish_cell.y_mid
    return math.hypot(x1-x2,y1-y2)

def reconstruct(came_from, current_node):
    try:
        p = reconstruct(came_from, came_from[current_node])
        return p + [current_node]
    except:
        return [current_node]

def get_neighbors(node, map_layout):
    x, y = node
    neighbors = []
    for d in [N,S,E,W]:
        if map_layout.cells[x][y].accessible[d]:
            dx, dy = CELL_IN_DIRECTION[d]
            neighbors.append((x+dx, y+dy))
    return neighbors

def create_empty_map(w,h):
    return [[0]*w for i in range(h)]

def create_ai_map(objects, walls):
    vertical_points = set([0,len(walls.layout)-2])
    horizontal_points = set([0, len(walls.layout[0])-2])
    objects_set = set()
    for j in xrange(len(walls.layout)):
        for i in xrange(len(walls.layout[0])):
            if walls.layout[j][i] in [wall_layout.POINT,
                                      wall_layout.OPEN_POINT]:
                horizontal_points.add(i)
                vertical_points.add(j)
    for key, obj in objects.items():
        horizontal_points.add(obj.map_coords[1])
        horizontal_points.add(obj.map_coords[1]+1)
        vertical_points.add(obj.map_coords[0])
        vertical_points.add(obj.map_coords[0]+1)
        objects_set.add(obj.map_coords)
    sorted_verticals = sorted(list(vertical_points))
    sorted_horizontals = sorted(list(horizontal_points))
    new_map = AIMap(sorted_verticals, sorted_horizontals, walls.layout, objects_set)
    return new_map
            
class AIMap:
    def __init__(self, sorted_verticals, sorted_horizontals, wall_layout, objects):
        self.sorted_verticals = sorted_verticals
        self.sorted_horizontals = sorted_horizontals
        w = len(sorted_horizontals)
        h = len(sorted_verticals)
        self.cells = [[None]*(h-1) for i in xrange(w-1)] 
        for i in xrange(w-1):
            for j in xrange(h-1):
                x1, y1 = sorted_horizontals[i], sorted_verticals[j]
                x2, y2 = sorted_horizontals[i+1], sorted_verticals[j+1]
                self.add_cell(i,j,AICell(x1,x2,y1,y2,wall_layout,objects))
        
    def add_cell(self, i, j, cell):
        self.cells[i][j] = cell

    def point_to_cell(self, position):
        x, y = position
        final_x = None
        final_y = None
        
        for i, cell_x in enumerate(self.sorted_verticals):
            if x < cell_x:
                final_x = i-1
                break
        final_y = None
        for j, cell_y in enumerate(self.sorted_horizontals):
            if y < cell_y:
                final_y = j-1
                break
        return (final_y, final_x)

class AICell:
    def __init__(self, x1, x2, y1, y2, layout, objects):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.x_mid = (x1 + x2)/2.0
        self.y_mid = (y1 + y2)/2.0
        self.accessible = {}
                
        nw = layout[y1][x1]
        sw = layout[y2][x1]
        ne = layout[y1][x2]
        se = layout[y2][x2]
        
        self.accessible[N] = accessible(nw, ne)
        self.accessible[S] = accessible(sw, se)
        self.accessible[E] = accessible(se, ne)
        self.accessible[W] = accessible(nw, sw)

        if x1 == 0 or (x1-1,y1) in objects:
            self.accessible[W] = False
        if y1 == 0 or (x1,y1-1) in objects:
            self.accessible[N] = False
        if y2 == len(layout)-2 or (x1,y2) in objects:
            self.accessible[S] = False
        if x2 == len(layout)-2 or (x2,y1) in objects:
            self.accessible[E] = False

    def __str__(self):
        n = "N:" + str(self.accessible[N])
        s = "S:" + str(self.accessible[S])
        e = "E:" + str(self.accessible[E])
        w = "W:" + str(self.accessible[W])
        return str((self.x1, self.y1)) + str((self.x2, self.y2)) + n + s + e + w
        
def accessible(corner_a, corner_b):
    if corner_a == wall_layout.EMPTY or corner_b == wall_layout.EMPTY:
        return True
    if corner_a == wall_layout.OPEN_POINT and corner_b in [wall_layout.VERTICAL, wall_layout.HORIZONTAL]:
        return True
    if corner_b == wall_layout.OPEN_POINT and corner_a in [wall_layout.VERTICAL, wall_layout.HORIZONTAL]:
        return True
    if corner_a not in [wall_layout.OPEN_POINT, wall_layout.EMPTY]:
        return False
    if corner_b not in [wall_layout.OPEN_POINT, wall_layout.EMPTY]:
        return False
    return True

def is_invalid_cell(cell):
    return cell[0] is None or cell[1] is None

class NoPathError(Exception):
    def __init__(self, destination):
        self.destination = str(destination)

    def __str__(self):
        return "No path to " + self.destination
