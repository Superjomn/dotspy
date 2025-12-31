"""Tests for diagram-specific components (UML, mind maps, etc.)."""

import unittest

from dotspy import Graph
from dotspy.diagrams import (
    MINDMAP_GRAPH,
    UML_GRAPH,
    AbstractClassNode,
    AggregationEdge,
    AssociationEdge,
    BranchEdge,
    ClassNode,
    CompositionEdge,
    DependencyEdge,
    ImplementsEdge,
    InheritanceEdge,
    InterfaceNode,
    MindNode,
    NoteEdge,
    NoteNode,
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

    def test_mindnode_basic(self):
        """Test basic MindNode creation."""
        with Graph("test_mindnode", styles=MINDMAP_GRAPH) as g:
            node = MindNode("Central Idea")

            dot = g.to_dot()
            self.assertIn("Central Idea", dot)
            self.assertIn('shape="box"', dot)

    def test_mindnode_with_preset_styles(self):
        """Test MindNode with preset style application."""
        from dotspy.diagrams.mindmap import BRANCH_STYLE, LEAF_STYLE, TOPIC_STYLE

        with Graph("test_styles", styles=MINDMAP_GRAPH) as g:
            topic = MindNode("Topic", styles=TOPIC_STYLE)
            branch = MindNode("Branch", styles=BRANCH_STYLE)
            leaf = MindNode("Leaf", styles=LEAF_STYLE)

            dot = g.to_dot()
            self.assertIn("Topic", dot)
            self.assertIn("Branch", dot)
            self.assertIn("Leaf", dot)

    def test_note_node(self):
        """Test NoteNode creation."""
        with Graph("test_note", styles=MINDMAP_GRAPH) as g:
            note = NoteNode("Important detail")

            dot = g.to_dot()
            self.assertIn("Important detail", dot)
            self.assertIn('shape="note"', dot)

    def test_note_auto_styling(self):
        """Test NoteNode auto-applies NoteEdge styling."""
        with Graph("test_note_auto", styles=MINDMAP_GRAPH) as g:
            main = MindNode("Main Topic")
            note = NoteNode("Side note")
            main >> note  # NoteEdge styling applied automatically

            dot = g.to_dot()
            self.assertIn('"Main Topic" -> "note_Side note"', dot)
            self.assertIn('style="dashed"', dot)
            self.assertIn('dir="none"', dot)

    def test_branch_edge(self):
        """Test BranchEdge styling."""
        with Graph("test_branch_edge", styles=MINDMAP_GRAPH) as g:
            root = MindNode("Root")
            branch = MindNode("Branch")

            root >> branch | BranchEdge()

            dot = g.to_dot()
            self.assertIn('"Root" -> "Branch"', dot)
            self.assertIn('dir="none"', dot)  # No arrows in mind maps

    def test_note_edge(self):
        """Test NoteEdge styling."""
        with Graph("test_note_edge", styles=MINDMAP_GRAPH) as g:
            node = MindNode("Main")
            note = NoteNode("Detail")

            node >> note | NoteEdge()

            dot = g.to_dot()
            self.assertIn('style="dashed"', dot)
            self.assertIn('dir="none"', dot)

    def test_manual_mindmap(self):
        """Test manual mind map construction."""
        with Graph("manual_mindmap", styles=MINDMAP_GRAPH) as g:
            root = MindNode("Project")
            frontend = MindNode("Frontend")
            backend = MindNode("Backend")
            react = MindNode("React")
            vue = MindNode("Vue")

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

    def test_tuple_fanout(self):
        """Test tuple fan-out syntax for creating multiple edges."""
        with Graph("tuple_fanout", styles=MINDMAP_GRAPH) as g:
            project = MindNode("Project")
            frontend = MindNode("Frontend")

            # Create edges to multiple nodes using tuple
            (
                project
                >> frontend
                >> (
                    MindNode("React"),
                    MindNode("Vue"),
                    MindNode("Angular"),
                )
            )

            dot = g.to_dot()
            self.assertIn("Project", dot)
            self.assertIn("Frontend", dot)
            self.assertIn("React", dot)
            self.assertIn("Vue", dot)
            self.assertIn("Angular", dot)
            # Verify edges exist
            self.assertIn('"Frontend" -> "React"', dot)
            self.assertIn('"Frontend" -> "Vue"', dot)
            self.assertIn('"Frontend" -> "Angular"', dot)

    def test_complex_mindmap_with_new_api(self):
        """Test complex mind map using new object-oriented API."""
        with Graph("complex_mindmap", styles=MINDMAP_GRAPH) as g:
            project = MindNode("Project Ideas")
            frontend = MindNode("Frontend")
            backend = MindNode("Backend")

            project >> (frontend, backend) | BranchEdge()
            frontend >> (MindNode("React"), MindNode("Vue"), MindNode("Angular"))
            backend >> (MindNode("Django"), MindNode("FastAPI"))

            dot = g.to_dot()
            self.assertIn("Project Ideas", dot)
            self.assertIn("Frontend", dot)
            self.assertIn("React", dot)
            self.assertIn("Django", dot)

    def test_mindmap_renders_with_graphviz(self):
        """End-to-end test: verify graphviz can render mind map."""
        with Graph("e2e_mindmap", styles=MINDMAP_GRAPH) as g:
            project = MindNode("Project Ideas")
            project >> (
                MindNode("Web App"),
                MindNode("Mobile App"),
                MindNode("DevOps"),
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
            topic = MindNode("Related Concept")

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
            MindNode("Test")
            dot2 = g2.to_dot()
            self.assertIn('splines="curved"', dot2)


if __name__ == "__main__":
    unittest.main()
