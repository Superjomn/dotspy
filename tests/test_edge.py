import unittest

from dotspy import Edge, EdgeStyle, Graph, Node


class TestEdge(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.__enter__()

    def tearDown(self):
        self.graph.__exit__()

    def test_edge_creation(self):
        n1 = Node("n1")
        n2 = Node("n2")
        e = Edge(n1, n2, color="red")
        self.assertEqual(e.source, n1)
        self.assertEqual(e.target, n2)
        self.assertEqual(e._attrs["color"], "red")

    def test_operator_syntax(self):
        n1 = Node("n1")
        n2 = Node("n2")
        # Now returns EdgeChain containing one edge
        chain = n1 >> n2
        self.assertEqual(len(chain.edges), 1)
        e = chain.edges[0]
        self.assertEqual(e.source, n1)
        self.assertEqual(e.target, n2)

    def test_edge_chaining(self):
        n1 = Node("n1")
        n2 = Node("n2")
        n3 = Node("n3")
        chain = n1 >> n2 >> n3
        self.assertEqual(len(chain.edges), 2)
        self.assertEqual(chain.edges[0].source, n1)
        self.assertEqual(chain.edges[0].target, n2)
        self.assertEqual(chain.edges[1].source, n2)
        self.assertEqual(chain.edges[1].target, n3)

    def test_style_chaining(self):
        n1 = Node("n1")
        n2 = Node("n2")
        chain = (n1 >> n2).set_styles(color="blue")
        self.assertEqual(chain.edges[0]._attrs["color"], "blue")

    def test_call_syntax(self):
        n1 = Node("n1")
        n2 = Node("n2")
        # Call syntax works on single Edge objects (created manually)
        e = Edge(n1, n2)(color="green")
        self.assertEqual(e._attrs["color"], "green")

        # Or via chain
        # Note: chain doesn't support __call__ yet based on implementation,
        # let's check if user requested it? No, just | dict.
        # But Edge itself supports it.

    def test_or_syntax_edge_style(self):
        n1 = Node("n1")
        n2 = Node("n2")
        style = EdgeStyle(style="dashed")
        chain = (n1 >> n2) | style
        self.assertEqual(chain.edges[0]._attrs["style"], "dashed")

    def test_or_syntax_dict(self):
        n1 = Node("n1")
        n2 = Node("n2")
        chain = (n1 >> n2) | {"color": "purple", "penwidth": 3}
        self.assertEqual(chain.edges[0]._attrs["color"], "purple")
        self.assertEqual(chain.edges[0]._attrs["penwidth"], 3)

    def test_chain_style_application(self):
        n1 = Node("n1")
        n2 = Node("n2")
        n3 = Node("n3")
        chain = n1 >> n2 >> n3 | {"color": "red"}
        for edge in chain.edges:
            self.assertEqual(edge._attrs["color"], "red")

    def test_getitem_syntax(self):
        n1 = Node("n1")
        n2 = Node("n2")
        style = EdgeStyle(penwidth=2)
        # Edge support
        e = Edge(n1, n2)[style]
        self.assertEqual(e._attrs["penwidth"], 2)
        # Chain support not explicitly requested via [], but | is preferred.

    def test_duplicate_edge_prevention(self):
        """Test that duplicate edges are not added to the graph."""
        n1 = Node("n1")
        n2 = Node("n2")

        # Add the same edge twice
        n1 >> n2
        n1 >> n2

        # Only one edge should be in the graph
        self.assertEqual(len(self.graph._edges), 1)

    def test_edges_with_different_attributes_are_duplicates(self):
        """Test that edges with same source/target are duplicates regardless of attributes."""
        n1 = Node("n1")
        n2 = Node("n2")

        # Add edges with different attributes
        Edge(n1, n2, color="red")
        Edge(n1, n2, color="blue")

        # Only first edge should be in the graph (duplicates based on source/target only)
        self.assertEqual(len(self.graph._edges), 1)
        # The first edge retains its original attributes
        self.assertEqual(self.graph._edges[0]._attrs["color"], "red")


if __name__ == "__main__":
    unittest.main()
