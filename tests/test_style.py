import unittest
from dotspy import NodeStyle, EdgeStyle, GraphStyle, Node, Edge, Graph
from dotspy.style import merge_styles

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

    def test_merge_styles_list(self):
        """Test merge_styles() with list of styles."""
        s1 = NodeStyle(color="red", shape="box")
        s2 = NodeStyle(color="blue", style="filled")
        s3 = NodeStyle(fontsize=12)
        
        result = merge_styles([s1, s2, s3])
        self.assertEqual(result["color"], "blue")  # s2 overrides s1
        self.assertEqual(result["shape"], "box")   # s1 kept
        self.assertEqual(result["style"], "filled") # s2 added
        self.assertEqual(result["fontsize"], 12)    # s3 added

    def test_node_with_multiple_styles(self):
        """Test Node accepts list of styles."""
        base = NodeStyle(shape="box", color="red")
        override = NodeStyle(color="blue", style="filled")
        
        with Graph("test"):
            n = Node("n1", styles=[base, override])
            self.assertEqual(n.attrs["color"], "blue")
            self.assertEqual(n.attrs["shape"], "box")
            self.assertEqual(n.attrs["style"], "filled")

    def test_edge_with_multiple_styles(self):
        """Test Edge accepts list of styles."""
        base = EdgeStyle(color="red", style="dashed")
        override = EdgeStyle(color="green", penwidth=2.0)
        
        with Graph("test") as g:
            n1 = Node("n1")
            n2 = Node("n2")
            e = Edge(n1, n2, styles=[base, override])
            
            self.assertEqual(e.attrs["color"], "green")
            self.assertEqual(e.attrs["style"], "dashed")
            self.assertEqual(e.attrs["penwidth"], 2.0)
            
            # Test __call__ update
            e(styles=[base, EdgeStyle(arrowhead="vee")])
            self.assertEqual(e.attrs["arrowhead"], "vee")
            # Note: calling e(...) updates existing attributes, so color is still green if not overwritten?
            # Wait, merge_styles returns updates. Then we update self. 
            # So if we call e([base...]), base has color="red". It overwrites.
            self.assertEqual(e.attrs["color"], "red") 

    def test_graph_with_multiple_styles(self):
        """Test Graph accepts list of styles."""
        base = GraphStyle(rankdir="TB", bgcolor="white")
        override = GraphStyle(rankdir="LR", fontname="Arial")
        
        g = Graph("test", styles=[base, override])
        self.assertEqual(g.attrs["rankdir"], "LR")
        self.assertEqual(g.attrs["bgcolor"], "white")
        self.assertEqual(g.attrs["fontname"], "Arial")

if __name__ == "__main__":
    unittest.main()
