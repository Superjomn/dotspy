import unittest
from dotspy import NodeStyle, EdgeStyle, GraphStyle

class TestStyle(unittest.TestCase):
    def test_style_attributes(self):
        s = NodeStyle(shape="box", color="red")
        d = s.to_dict()
        self.assertEqual(d["shape"], "box")
        self.assertEqual(d["color"], "red")

    def test_merge(self):
        s1 = NodeStyle(color="red", shape="box")
        s2 = NodeStyle(color="blue", style="filled")
        s3 = s1.merge(s2)
        
        d = s3.to_dict()
        self.assertEqual(d["color"], "blue")  # s2 overrides s1
        self.assertEqual(d["shape"], "box")   # s1 kept
        self.assertEqual(d["style"], "filled") # s2 added

    def test_edge_style(self):
        s = EdgeStyle(arrowhead="none")
        self.assertEqual(s.to_dict()["arrowhead"], "none")

if __name__ == "__main__":
    unittest.main()
