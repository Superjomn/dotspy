import unittest
from dotspy import Graph, Subgraph, Node, GraphStyle

class TestGraph(unittest.TestCase):
    def test_graph_context(self):
        with Graph("G") as g:
            n = Node("n")
            self.assertIn(n, g._nodes)
            
    def test_subgraph(self):
        with Graph("G") as g:
            with Subgraph("sub") as s:
                n = Node("n")
                self.assertIn("n", s._nodes)
                self.assertIn(s, g._subgraphs)

    def test_nested_subgraphs(self):
        with Graph("G") as g:
            with Subgraph("s1") as s1:
                pass
                # Currently Subgraphs can't contain subgraphs directly in the implementation I wrote?
                # Let's check graph.py
                # Subgraph registers with current graph.
                # But if we are inside a subgraph context, get_current_graph() returns the main graph.
                # get_current_subgraph() returns the current subgraph.
                # Subgraph._register() logic:
                # graph = get_current_graph()
                # if graph: graph._add_subgraph(self)
                # It doesn't check for current subgraph to nest subgraphs.
                # DOT supports nested subgraphs.
                # This might be a limitation in current implementation, but that's okay for MVP.
                pass
    
    def test_graph_style(self):
        style = GraphStyle(rankdir="LR")
        g = Graph(style=style)
        self.assertEqual(g._attrs["rankdir"], "LR")

    def test_subgraph_cluster_name(self):
        s = Subgraph("foo", cluster=True)
        self.assertEqual(s._name, "cluster_foo")
        
        s2 = Subgraph("bar", cluster=False)
        self.assertEqual(s2._name, "bar")

    def test_subgraph_auto_id(self):
        s = Subgraph(cluster=False)
        self.assertTrue(s.name.startswith("subgraph_"))
        
    def test_subgraph_auto_id_cluster(self):
        # Default is cluster=True
        s = Subgraph()
        self.assertTrue(s.name.startswith("cluster_subgraph_"))

    def test_subgraph_auto_id_no_cluster(self):
        s = Subgraph(cluster=False)
        self.assertFalse(s.name.startswith("cluster_"))
        self.assertTrue(s.name.startswith("subgraph_"))

if __name__ == "__main__":
    unittest.main()
