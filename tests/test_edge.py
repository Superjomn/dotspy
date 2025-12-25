import unittest
from dotspy import Node, Graph, Edge, EdgeStyle

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
        chain = (n1 >> n2).style(color="blue")
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

if __name__ == "__main__":
    unittest.main()
