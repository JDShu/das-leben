import unittest

from das_leben.ai import *
from das_leben.wall_layout import WallLayout

class TestAI(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_empty_map(self):
        wall_data = WallLayout()
        wall_data.load_textfile("tests/ai.wall")
        ai_map = create_ai_map(None, wall_data)
        self.assertEqual(len(ai_map.cells), 1)
        self.assertEqual(len(ai_map.cells[0]), 1)
        cell = ai_map.cells[0][0]
        self.assertEqual(cell.accessible[N], False)
        self.assertEqual(cell.accessible[S], False)
        self.assertEqual(cell.accessible[E], False)
        self.assertEqual(cell.accessible[W], False) 

    def test_one_room(self):
        wall_data = WallLayout()
        wall_data.load_textfile("tests/one_room.wall")
        ai_map = create_ai_map(None, wall_data)
        self.assertEqual(len(ai_map.cells), 1)
        self.assertEqual(len(ai_map.cells[0]), 2)
        cell = ai_map.cells[0][0]
        self.assertEqual(cell.accessible[N], False)
        self.assertEqual(cell.accessible[S], False)
        self.assertEqual(cell.accessible[E], False)
        self.assertEqual(cell.accessible[W], False) 

    def test_three_sided_room(self):
        wall_data = WallLayout()
        wall_data.load_textfile("tests/three_sided_room.wall")
        ai_map = create_ai_map(None, wall_data)
        self.assertEqual(len(ai_map.cells), 1)
        self.assertEqual(len(ai_map.cells[0]), 2)
        cell = ai_map.cells[0][0]
        self.assertEqual(cell.accessible[N], False)
        self.assertEqual(cell.accessible[S], True)
        self.assertEqual(cell.accessible[E], False)
        self.assertEqual(cell.accessible[W], False) 

if __name__ == '__main__':
    unittest.main()
