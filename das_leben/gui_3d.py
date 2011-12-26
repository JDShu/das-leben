from pandac.PandaModules import CollisionHandlerQueue, CollisionTraverser, \
     CollisionNode, CollisionRay, CollisionPlane, CollisionTube, Vec3, Plane, Point3 

class Gui3D:
    def __init__(self, game_data, gfx_manager):
        self.game_data = game_data
        self.gui_traverser = CollisionTraverser()
        self.handler = CollisionHandlerQueue()
        self.selectable_objects = {}
        for cid, model in gfx_manager.character_models.items():
            new_collision_node = CollisionNode('person_' + str(cid))
            new_collision_node.addSolid(CollisionTube(0, 0, 0.5, 0, 0, 1.5, 0.5))
            new_collision_nodepath = model.attachNewNode(new_collision_node)
            new_collision_nodepath.setTag("type","character")
            new_collision_nodepath.setTag("id",str(cid))
        
        picker_node = CollisionNode('mouseRay')
        picker_np = camera.attachNewNode(picker_node)
        self.picker_ray = CollisionRay()
        picker_node.addSolid(self.picker_ray)
        self.gui_traverser.addCollider(picker_np, self.handler)
        self.floor = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        self.floor_np = render.attachNewNode(CollisionNode('floor'))
        self.floor_np.node().addSolid(self.floor)
        
    def mouse_click(self):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.picker_ray.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            self.gui_traverser.traverse(render)
            num_entries = self.handler.getNumEntries()
            if num_entries > 0:
                self.handler.sortEntries()
                entry = self.handler.getEntry(0)
                selected = entry.getIntoNodePath()
                selected_type = selected.getTag("type")
                if selected_type == "character":
                    self.game_data.select_character(int(selected.getTag("id")))
