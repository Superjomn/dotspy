import unittest
from dotspy import Node, Graph, NodeStyle

class TestNode(unittest.TestCase):
    def setUp(self):
        # We need a graph context for nodes to register, mostly
        self.graph = Graph()
        self.graph.__enter__()

    def tearDown(self):
        self.graph.__exit__()

    def test_node_creation(self):
        n = Node("test")
        self.assertEqual(n.name, "test")
        self.assertEqual(n.attrs, {})

    def test_auto_naming(self):
        n1 = Node()
        n2 = Node()
        self.assertNotEqual(n1.name, n2.name)
        self.assertTrue(n1.name.startswith("node_"))

    def test_node_attributes(self):
        n = Node("test", shape="box", color="red")
        self.assertEqual(n.attrs["shape"], "box")
        self.assertEqual(n.attrs["color"], "red")

    def test_node_style_object(self):
        style = NodeStyle(shape="circle", color="blue")
        n = Node("test", styles=style)
        self.assertEqual(n.attrs["shape"], "circle")
        self.assertEqual(n.attrs["color"], "blue")

    def test_context_style(self):
        style = NodeStyle(fontname="Arial")
        with style:
            n = Node("test")
        self.assertEqual(n.attrs["fontname"], "Arial")
        
        n2 = Node("test2")
        self.assertNotIn("fontname", n2.attrs)

    def test_node_nstyle_parameter(self):
        style = NodeStyle(shape="diamond", color="green")
        n = Node("test_nstyle", styles=style)
        self.assertEqual(n.attrs["shape"], "diamond")
        self.assertEqual(n.attrs["color"], "green")

    def test_node_styles_priority(self):
        style1 = NodeStyle(shape="box")
        style2 = NodeStyle(shape="circle")
        # style2 should take precedence over style1 in list
        n = Node("test_prec", styles=[style1, style2])
        self.assertEqual(n.attrs["shape"], "circle")

if __name__ == "__main__":
    unittest.main()
