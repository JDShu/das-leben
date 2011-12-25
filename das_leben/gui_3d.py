from pandac.PandaModules import CollisionHandlerQueue, CollisionTraverser, \
     CollisionNode, CollisionRay, CollisionPlane, Vec3, Plane, Point3 

class Gui3D:
    def __init__(self, camera):
        self.gui_traverser = CollisionTraverser()
        self.handler = CollisionHandlerQueue()
        
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
            for i in range(num_entries):
                entry = self.handler.getEntry(i)
                if entry.hasInto():
                    print entry.getSurfacePoint(render)
