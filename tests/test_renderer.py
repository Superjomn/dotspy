import unittest

from dotspy import Edge, Graph, Node, renderer


class TestRenderer(unittest.TestCase):
    def test_escape_string(self):
        self.assertEqual(renderer.escape_string('foo"bar'), 'foo\\"bar')
        self.assertEqual(renderer.escape_string("foo\\bar"), "foo\\\\bar")

    def test_format_attrs(self):
        attrs = {"label": 'foo"bar', "color": "red", "weight": 1}
        s = renderer.format_attrs(attrs)
        # Order is insertion order in recent Pythons
        self.assertIn('label="foo\\"bar"', s)
        self.assertIn('color="red"', s)
        self.assertIn('weight="1"', s)

    def test_render_node(self):
        n = Node("n1", label="Node 1")
        s = renderer.render_node(n)
        self.assertIn('"n1"', s)
        self.assertIn('label="Node 1"', s)

    def test_render_edge_digraph(self):
        n1 = Node("n1")
        n2 = Node("n2")
        e = Edge(n1, n2)
        s = renderer.render_edge(e, is_digraph=True)
        self.assertIn('"n1" -> "n2"', s)

    def test_render_edge_graph(self):
        n1 = Node("n1")
        n2 = Node("n2")
        e = Edge(n1, n2)
        s = renderer.render_edge(e, is_digraph=False)
        self.assertIn('"n1" -- "n2"', s)

    def test_render_graph(self):
        with Graph("G") as g:
            n1 = Node("n1")
            n2 = Node("n2")
            n1 >> n2

        dot = g.to_dot()
        self.assertIn('digraph "G" {', dot)
        self.assertIn('"n1" -> "n2"', dot)
        self.assertIn("}", dot)


if __name__ == "__main__":
    unittest.main()
