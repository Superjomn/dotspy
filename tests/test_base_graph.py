import unittest

from dotspy import BaseGraph, Graph, Node, Subgraph


class TestBaseGraph(unittest.TestCase):
    def test_simple_node_group(self):
        """Test basic node grouping without subgraph creation."""

        class MyNodes(BaseGraph):
            @BaseGraph.add_node
            def _(self):
                return Node("NodeA")

            @BaseGraph.add_node
            def _(self):
                return Node("NodeB")

        # Should not create any global graph/subgraph on its own
        nodes = MyNodes()

        self.assertEqual(len(nodes._nodes), 2)
        self.assertIsInstance(nodes.NodeA, Node)
        self.assertEqual(nodes.NodeA.name, "NodeA")
        self.assertEqual(nodes.NodeB.name, "NodeB")

        # Verify no subgraph created
        self.assertIsNone(nodes._subgraph)

    def test_subgraph_wrapping(self):
        """Test wrapping nodes in a subgraph."""

        class MyCluster(BaseGraph):
            @BaseGraph.add_node
            def _(self):
                return Node("ServiceA")

        with Graph() as g:
            # Create subgraph via use_subgraph=True
            cluster = MyCluster(label="Backend", use_subgraph=True)

            # Check internal subgraph created
            self.assertIsNotNone(cluster._subgraph)
            self.assertIsInstance(cluster._subgraph, Subgraph)
            self.assertEqual(
                cluster._subgraph.name, "cluster_Backend"
            )  # default cluster prefix logic

            # Check node is in subgraph
            self.assertIn("ServiceA", cluster._subgraph._nodes)

            # Check attribute access delegation
            self.assertEqual(cluster.ServiceA.name, "ServiceA")

    def test_duplicate_names_error(self):
        """Test that duplicate node names raise ValueError."""

        class BadGraph(BaseGraph):
            @BaseGraph.add_node
            def _(self):
                return Node("SameName")

            @BaseGraph.add_node
            def _(self):
                return Node("SameName")

        with self.assertRaises(ValueError):
            BadGraph()

    def test_context_manager_usage(self):
        """Test context manager delegation."""

        class MyGroup(BaseGraph):
            @BaseGraph.add_node
            def _(self):
                return Node("Root")

        # Case 1: use_subgraph=False (returns self)
        group = MyGroup(use_subgraph=False)
        with group as g:
            self.assertIs(g, group)

        # Case 2: use_subgraph=True (returns subgraph)
        with Graph():
            group_sub = MyGroup(label="Group", use_subgraph=True)
            with group_sub as s:
                self.assertIsInstance(s, Subgraph)
                self.assertEqual(s.name, "cluster_Group")

    def test_edge_building(self):
        """Test using attributes for edge building."""

        class Workflow(BaseGraph):
            @BaseGraph.add_node
            def _(self):
                return Node("Start")

            @BaseGraph.add_node
            def _(self):
                return Node("End")

        with Graph() as g:
            wf = Workflow()
            # This uses the >> operator on Node
            edge = wf.Start >> wf.End

            # Check edge was added to graph
            self.assertEqual(len(g._edges), 1)
            self.assertEqual(g._edges[0].source.name, "Start")
            self.assertEqual(g._edges[0].target.name, "End")

    def test_inheritance(self):
        """Test inheriting from another BaseGraph subclass."""

        class Parent(BaseGraph):
            @BaseGraph.add_node
            def _(self):
                return Node("ParentNode")

        class Child(Parent):
            @BaseGraph.add_node
            def _(self):
                return Node("ChildNode")

        c = Child()
        self.assertIn("ParentNode", c._nodes)
        self.assertIn("ChildNode", c._nodes)
