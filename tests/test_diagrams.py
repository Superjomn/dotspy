"""Tests for diagram-specific components (UML, mind maps, etc.)."""

import unittest

from dotspy import Graph
from dotspy.diagrams import (
    MINDMAP_GRAPH,
    RADIAL_MINDMAP_GRAPH,
    UML_GRAPH,
    AbstractClassNode,
    AggregationEdge,
    AssociationEdge,
    BranchEdge,
    BranchNode,
    ClassNode,
    CompositionEdge,
    DependencyEdge,
    ImplementsEdge,
    InheritanceEdge,
    InterfaceNode,
    LeafNode,
    TopicNode,
    mindmap,
    radial_mindmap,
)
from dotspy.utils import render_to_svg


class TestUMLDiagrams(unittest.TestCase):
    """Test UML class diagram components."""

    def test_class_node_basic(self):
        """Test basic ClassNode creation."""
        with Graph("test_uml", styles=UML_GRAPH) as g:
            animal = ClassNode(
                "Animal",
                attributes=["+ name: str", "- age: int"],
                methods=["+ speak(): void", "+ move(): void"],
            )

            # Verify DOT generation
            dot = g.to_dot()
            self.assertIn("Animal", dot)
            self.assertIn("TABLE", dot)
            self.assertIn("name: str", dot)
            self.assertIn("speak(): void", dot)

    def test_interface_node(self):
        """Test InterfaceNode with stereotype."""
        with Graph("test_interface", styles=UML_GRAPH) as g:
            drawable = InterfaceNode("Drawable", methods=["+ draw(): void"])

            dot = g.to_dot()
            self.assertIn("Drawable", dot)
            self.assertIn("interface", dot)
            self.assertIn("draw(): void", dot)

    def test_abstract_class_node(self):
        """Test AbstractClassNode."""
        with Graph("test_abstract", styles=UML_GRAPH) as g:
            shape = AbstractClassNode(
                "Shape", attributes=["+ color: str"], methods=["+ getArea(): float"]
            )

            dot = g.to_dot()
            self.assertIn("Shape", dot)
            self.assertIn("abstract", dot)
            self.assertIn("getArea", dot)

    def test_inheritance_edge(self):
        """Test inheritance relationship."""
        with Graph("test_inheritance", styles=UML_GRAPH) as g:
            animal = ClassNode("Animal", methods=["+ speak(): void"])
            dog = ClassNode("Dog", methods=["+ bark(): void"])

            dog >> animal | InheritanceEdge()

            dot = g.to_dot()
            self.assertIn('"Dog" -> "Animal"', dot)
            self.assertIn('arrowhead="empty"', dot)

    def test_implements_edge(self):
        """Test interface implementation relationship."""
        with Graph("test_implements", styles=UML_GRAPH) as g:
            drawable = InterfaceNode("Drawable", methods=["+ draw(): void"])
            circle = ClassNode("Circle", methods=["+ draw(): void"])

            circle >> drawable | ImplementsEdge()

            dot = g.to_dot()
            self.assertIn('"Circle" -> "Drawable"', dot)
            self.assertIn('arrowhead="empty"', dot)
            self.assertIn('style="dashed"', dot)

    def test_composition_edge(self):
        """Test composition relationship (filled diamond)."""
        with Graph("test_composition", styles=UML_GRAPH) as g:
            car = ClassNode("Car")
            engine = ClassNode("Engine")

            car >> engine | CompositionEdge()

            dot = g.to_dot()
            self.assertIn('"Car" -> "Engine"', dot)
            self.assertIn('arrowtail="diamond"', dot)

    def test_aggregation_edge(self):
        """Test aggregation relationship (hollow diamond)."""
        with Graph("test_aggregation", styles=UML_GRAPH) as g:
            department = ClassNode("Department")
            employee = ClassNode("Employee")

            department >> employee | AggregationEdge()

            dot = g.to_dot()
            self.assertIn('"Department" -> "Employee"', dot)
            self.assertIn('arrowtail="odiamond"', dot)

    def test_association_edge(self):
        """Test association relationship with multiplicity."""
        with Graph("test_association", styles=UML_GRAPH) as g:
            student = ClassNode("Student")
            course = ClassNode("Course")

            student >> course | AssociationEdge(
                label="enrolls in", multiplicity_source="*", multiplicity_target="*"
            )

            dot = g.to_dot()
            self.assertIn('"Student" -> "Course"', dot)
            self.assertIn('label="enrolls in"', dot)
            self.assertIn('taillabel="*"', dot)
            self.assertIn('headlabel="*"', dot)

    def test_dependency_edge(self):
        """Test dependency relationship."""
        with Graph("test_dependency", styles=UML_GRAPH) as g:
            client = ClassNode("Client")
            service = ClassNode("Service")

            client >> service | DependencyEdge(label="uses")

            dot = g.to_dot()
            self.assertIn('"Client" -> "Service"', dot)
            self.assertIn('style="dashed"', dot)
            self.assertIn('label="uses"', dot)

    def test_complete_uml_diagram(self):
        """Test a complete UML class diagram with multiple relationships."""
        with Graph("complete_uml", styles=UML_GRAPH) as g:
            # Create classes
            animal = ClassNode("Animal", methods=["+ speak(): void"])
            dog = ClassNode("Dog", methods=["+ bark(): void"])
            cat = ClassNode("Cat", methods=["+ meow(): void"])

            # Create inheritance
            dog >> animal | InheritanceEdge()
            cat >> animal | InheritanceEdge()

            # Verify complete DOT structure
            dot = g.to_dot()
            self.assertIn("Animal", dot)
            self.assertIn("Dog", dot)
            self.assertIn("Cat", dot)
            self.assertIn('rankdir="TB"', dot)
            self.assertIn('splines="ortho"', dot)

    def test_uml_renders_with_graphviz(self):
        """End-to-end test: verify graphviz can render UML diagram."""
        with Graph("e2e_uml", styles=UML_GRAPH) as g:
            vehicle = ClassNode("Vehicle", attributes=["+ speed: float"])
            car = ClassNode("Car", attributes=["+ doors: int"])
            engine = ClassNode("Engine")

            car >> vehicle | InheritanceEdge()
            car >> engine | CompositionEdge()

            # This will raise if graphviz rejects the DOT
            svg = render_to_svg(g.to_dot())
            self.assertIn("<svg", svg)
            self.assertIn("Vehicle", svg)


class TestMindMaps(unittest.TestCase):
    """Test mind map components."""

    def test_topic_node(self):
        """Test TopicNode creation."""
        with Graph("test_topic", styles=MINDMAP_GRAPH) as g:
            root = TopicNode("Central Idea")

            dot = g.to_dot()
            self.assertIn("Central Idea", dot)
            self.assertIn('shape="ellipse"', dot)

    def test_branch_node(self):
        """Test BranchNode creation."""
        with Graph("test_branch", styles=MINDMAP_GRAPH) as g:
            branch = BranchNode("Main Branch")

            dot = g.to_dot()
            self.assertIn("Main Branch", dot)
            self.assertIn('shape="box"', dot)

    def test_leaf_node(self):
        """Test LeafNode creation."""
        with Graph("test_leaf", styles=MINDMAP_GRAPH) as g:
            leaf = LeafNode("Detail")

            dot = g.to_dot()
            self.assertIn("Detail", dot)
            self.assertIn('shape="box"', dot)

    def test_branch_edge(self):
        """Test BranchEdge styling."""
        with Graph("test_branch_edge", styles=MINDMAP_GRAPH) as g:
            root = TopicNode("Root")
            branch = BranchNode("Branch")

            root >> branch | BranchEdge()

            dot = g.to_dot()
            self.assertIn('"Root" -> "Branch"', dot)
            self.assertIn('dir="none"', dot)  # No arrows in mind maps

    def test_manual_mindmap(self):
        """Test manual mind map construction."""
        with Graph("manual_mindmap", styles=MINDMAP_GRAPH) as g:
            root = TopicNode("Project")
            frontend = BranchNode("Frontend")
            backend = BranchNode("Backend")
            react = LeafNode("React")
            vue = LeafNode("Vue")

            root >> frontend | BranchEdge()
            root >> backend | BranchEdge()
            frontend >> react | BranchEdge()
            frontend >> vue | BranchEdge()

            dot = g.to_dot()
            self.assertIn("Project", dot)
            self.assertIn("Frontend", dot)
            self.assertIn("Backend", dot)
            self.assertIn("React", dot)
            self.assertIn("Vue", dot)
            self.assertIn('rankdir="LR"', dot)
            self.assertIn('splines="curved"', dot)

    def test_mindmap_helper_with_lists(self):
        """Test mindmap() helper function with list values."""
        with Graph("helper_mindmap", styles=MINDMAP_GRAPH) as g:
            mindmap(
                {
                    "Project": {
                        "Frontend": ["React", "Vue", "Angular"],
                        "Backend": ["Python", "Go"],
                    }
                }
            )

            dot = g.to_dot()
            self.assertIn("Project", dot)
            self.assertIn("Frontend", dot)
            self.assertIn("Backend", dot)
            self.assertIn("React", dot)
            self.assertIn("Python", dot)

    def test_mindmap_helper_nested_dict(self):
        """Test mindmap() helper with nested dictionaries."""
        with Graph("nested_mindmap", styles=MINDMAP_GRAPH) as g:
            mindmap(
                {
                    "Tech Stack": {
                        "Frontend": {"JavaScript": ["React", "Vue"], "TypeScript": []},
                        "Backend": {"Python": ["Django", "Flask"]},
                    }
                }
            )

            dot = g.to_dot()
            self.assertIn("Tech Stack", dot)
            self.assertIn("Frontend", dot)
            self.assertIn("JavaScript", dot)
            self.assertIn("React", dot)
            self.assertIn("Django", dot)

    def test_radial_mindmap(self):
        """Test radial mind map with twopi layout."""
        with Graph("radial", styles=RADIAL_MINDMAP_GRAPH) as g:
            radial_mindmap(
                {
                    "Central": {
                        "Branch1": ["Item A", "Item B"],
                        "Branch2": ["Item C", "Item D"],
                    }
                }
            )

            dot = g.to_dot()
            self.assertIn("Central", dot)
            self.assertIn("Branch1", dot)
            self.assertIn("Item A", dot)
            self.assertIn('layout="twopi"', dot)

    def test_mindmap_renders_with_graphviz(self):
        """End-to-end test: verify graphviz can render mind map."""
        with Graph("e2e_mindmap", styles=MINDMAP_GRAPH) as g:
            mindmap(
                {
                    "Project Ideas": {
                        "Web App": ["Frontend", "Backend", "Database"],
                        "Mobile App": ["iOS", "Android"],
                        "DevOps": ["CI/CD", "Monitoring"],
                    }
                }
            )

            # This will raise if graphviz rejects the DOT
            svg = render_to_svg(g.to_dot())
            self.assertIn("<svg", svg)
            self.assertIn("Project Ideas", svg)


class TestDiagramIntegration(unittest.TestCase):
    """Integration tests combining different diagram types."""

    def test_mixed_nodes_in_graph(self):
        """Test using both UML and mind map nodes in same graph (unusual but valid)."""
        with Graph("mixed") as g:
            cls = ClassNode("MyClass", methods=["+ method(): void"])
            topic = TopicNode("Related Concept")

            cls >> topic

            dot = g.to_dot()
            self.assertIn("MyClass", dot)
            self.assertIn("Related Concept", dot)

    def test_graph_style_applied_correctly(self):
        """Test that UML_GRAPH and MINDMAP_GRAPH styles are applied."""
        with Graph("uml_styled", styles=UML_GRAPH) as g1:
            ClassNode("Test")
            dot1 = g1.to_dot()
            self.assertIn('splines="ortho"', dot1)

        with Graph("mindmap_styled", styles=MINDMAP_GRAPH) as g2:
            TopicNode("Test")
            dot2 = g2.to_dot()
            self.assertIn('splines="curved"', dot2)


if __name__ == "__main__":
    unittest.main()
