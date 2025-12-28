import unittest
from dotspy import Graph, Node, Subgraph, LR_GRAPH, BOX_NODE, RED_EDGE, EdgeStyle

class TestIntegration(unittest.TestCase):
    def test_complex_graph(self):
        with Graph("integration_test", styles=LR_GRAPH) as g:
            start = Node("start", shape="circle")
            end = Node("end", shape="doublecircle")
            
            with Subgraph("cluster_main") as sub:
                process1 = Node("process1", styles=BOX_NODE)
                process2 = Node("process2", styles=BOX_NODE)
                
                (process1 >> process2) | RED_EDGE
            
            start >> process1
            process2 >> end
            
            dot = g.to_dot()
            
            self.assertIn('rankdir="LR"', dot)
            self.assertIn('subgraph "cluster_main"', dot)
            self.assertIn('"process1" -> "process2"', dot)
            self.assertIn('color="red"', dot)

if __name__ == "__main__":
    unittest.main()
