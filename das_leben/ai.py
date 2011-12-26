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

from direct.task import Task
from panda3d.ai import AIWorld, AICharacter

class AI:

    def __init__(self, game_data, character_models):
        self.ai_world = AIWorld(render)
        self.character_catalog = {}
        for character_id, model in character_models.items():
            new_ai = AICharacter("character", model, 10, 0.05, 1)
            self.character_catalog[character_id] = AIData(new_ai)
            self.ai_world.addAiChar(new_ai)

        taskMgr.add(self.update,"AIUpdate")

    def begin_move(self, character_id, destination):
        character = self.character_catalog[character_id]
        character.destination = destination
        character.start_moving()
        print "going to", destination
                
    def stop_move(self, character_id):
        pass

    def update(self, task):
        self.ai_world.update()
        return Task.cont

class AIData:

    def __init__(self, character):
        self.character = character
        self.behavior = self.character.getAiBehaviors()
        self.behavior.initPathFind(os.path.join("data","games","navmesh.csv"))
        self.destination = None

    def start_moving(self):
        self.behavior.pathFindTo(self.destination, "addPath")
