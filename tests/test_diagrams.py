"""Tests for diagram-specific components (UML, mind maps, etc.)."""

import unittest

from dotspy import Graph, Subgraph
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
    UMLNoteEdge,
    UMLNoteNode,
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

    def test_text_wrapping_long_attributes(self):
        """Test that long attributes are wrapped to prevent wide nodes."""
        with Graph("test_wrapping", styles=UML_GRAPH) as g:
            node = ClassNode(
                "ComplexClass",
                attributes=[
                    "- very_long_configuration_parameter_that_makes_the_node_extremely_wide: Dict[str, Any]",
                    "- short: int",
                ],
            )

            dot = g.to_dot()
            # Check that wrapping occurred (BR tags present)
            self.assertIn("<BR ALIGN='LEFT'/>", dot)
            # Check that indentation is applied
            self.assertIn("&nbsp;&nbsp;", dot)
            # Short attributes should not be wrapped
            self.assertIn("short: int", dot)

    def test_text_wrapping_long_methods(self):
        """Test that long method signatures are wrapped."""
        with Graph("test_method_wrap", styles=UML_GRAPH) as g:
            node = ClassNode(
                "Service",
                methods=[
                    "+ perform_complex_operation(param1: str, param2: int, param3: List[str], param4: Dict[str, Any]): Result"
                ],
            )

            dot = g.to_dot()
            # Method should be wrapped at commas
            self.assertIn("<BR ALIGN='LEFT'/>", dot)
            # Check that params are split (looking for continuation)
            self.assertIn("param1", dot)
            self.assertIn("param2", dot)

    def test_text_wrapping_custom_width(self):
        """Test custom wrap_width parameter."""
        with Graph("test_custom_width", styles=UML_GRAPH) as g:
            # Use very narrow width to force wrapping
            node = ClassNode(
                "NarrowNode",
                attributes=["- medium_length_attribute: str"],
                wrap_width=20,
            )

            dot = g.to_dot()
            # With width=20, this should wrap
            self.assertIn("<BR ALIGN='LEFT'/>", dot)

    def test_text_wrapping_interface_node(self):
        """Test that InterfaceNode also supports text wrapping."""
        with Graph("test_interface_wrap", styles=UML_GRAPH) as g:
            node = InterfaceNode(
                "ComplexInterface",
                methods=[
                    "+ execute_service_request(request_id: str, payload: Dict[str, Any], timeout: int): Response"
                ],
            )

            dot = g.to_dot()
            self.assertIn("<BR ALIGN='LEFT'/>", dot)

    def test_text_wrapping_abstract_class_node(self):
        """Test that AbstractClassNode also supports text wrapping."""
        with Graph("test_abstract_wrap", styles=UML_GRAPH) as g:
            node = AbstractClassNode(
                "AbstractBase",
                attributes=[
                    "# protected_long_configuration_with_very_detailed_type: Dict[str, List[Tuple[int, str]]]"
                ],
            )

            dot = g.to_dot()
            self.assertIn("<BR ALIGN='LEFT'/>", dot)

    def test_uml_note_node(self):
        """Test UMLNoteNode creation and styling."""
        with Graph("test_uml_note", styles=UML_GRAPH) as g:
            note = UMLNoteNode("This is a documentation note")

            dot = g.to_dot()
            self.assertIn("This is a documentation note", dot)
            self.assertIn('shape="note"', dot)
            self.assertIn('fillcolor="lightyellow"', dot)

    def test_uml_note_edge(self):
        """Test UMLNoteEdge styling for note connections."""
        with Graph("test_uml_note_edge", styles=UML_GRAPH) as g:
            user = ClassNode("User", attributes=["+ name: str"])
            note = UMLNoteNode("Represents a system user")

            user >> note | UMLNoteEdge()

            dot = g.to_dot()
            # Note name is truncated to first 20 chars
            self.assertIn('"User" -> "note_Represents a system "', dot)
            self.assertIn('style="dashed"', dot)
            self.assertIn('dir="none"', dot)

    def test_static_member_formatting(self):
        """Test {static} modifier renders as underlined."""
        with Graph("test_static_member", styles=UML_GRAPH) as g:
            cls = ClassNode(
                "Singleton",
                attributes=["{static} - instance: Singleton"],
                methods=["{static} + getInstance(): Singleton"],
            )

            dot = g.to_dot()
            # Check for underline HTML tags
            self.assertIn("<U>", dot)
            self.assertIn("</U>", dot)
            self.assertIn("instance: Singleton", dot)
            self.assertIn("getInstance(): Singleton", dot)

    def test_abstract_member_formatting(self):
        """Test {abstract} modifier renders as italic."""
        with Graph("test_abstract_member", styles=UML_GRAPH) as g:
            cls = ClassNode(
                "Shape",
                methods=["{abstract} + draw(): void", "{abstract} + getArea(): float"],
            )

            dot = g.to_dot()
            # Check for italic HTML tags
            self.assertIn("<I>", dot)
            self.assertIn("</I>", dot)
            self.assertIn("draw(): void", dot)
            self.assertIn("getArea(): float", dot)

    def test_mixed_member_modifiers(self):
        """Test mixing static and abstract modifiers in same class."""
        with Graph("test_mixed_modifiers", styles=UML_GRAPH) as g:
            cls = ClassNode(
                "MixedClass",
                attributes=[
                    "{static} - count: int",
                    "+ name: str",
                ],
                methods=[
                    "{abstract} + process(): void",
                    "{static} + getCount(): int",
                    "+ getName(): str",
                ],
            )

            dot = g.to_dot()
            # Both underline and italic should be present
            self.assertIn("<U>", dot)
            self.assertIn("<I>", dot)
            # Regular members should also be present
            self.assertIn("name: str", dot)
            self.assertIn("getName(): str", dot)

    def test_spot_icon_default_colors(self):
        """Test spot icons with default colors."""
        with Graph("test_spot_defaults", styles=UML_GRAPH) as g:
            class_c = ClassNode("MyClass", spot="C")
            interface_i = ClassNode("MyInterface", spot="I")
            abstract_a = ClassNode("MyAbstract", spot="A")
            enum_e = ClassNode("MyEnum", spot="E")

            dot = g.to_dot()
            # Check that spot letters are in the output with parentheses
            self.assertIn("(C)", dot)
            self.assertIn("(I)", dot)
            self.assertIn("(A)", dot)
            self.assertIn("(E)", dot)
            # Check for default colors
            self.assertIn("BGCOLOR='lightblue'", dot)
            self.assertIn("BGCOLOR='lightyellow'", dot)
            self.assertIn("BGCOLOR='lightgray'", dot)
            self.assertIn("BGCOLOR='lightgreen'", dot)

    def test_spot_icon_custom_color(self):
        """Test spot icon with custom color override."""
        with Graph("test_spot_custom", styles=UML_GRAPH) as g:
            cls = ClassNode("CustomClass", spot="X", spot_color="pink")

            dot = g.to_dot()
            self.assertIn("(X)", dot)
            self.assertIn("BGCOLOR='pink'", dot)

    def test_spot_icon_with_stereotype(self):
        """Test spot icon combined with stereotype."""
        with Graph("test_spot_stereotype", styles=UML_GRAPH) as g:
            iface = InterfaceNode("Drawable", methods=["+ draw(): void"])
            # InterfaceNode has stereotype="interface" built-in

            dot = g.to_dot()
            self.assertIn("interface", dot)
            self.assertIn("Drawable", dot)

    def test_comprehensive_uml_features(self):
        """Test all new features together in one diagram."""
        with Graph("test_comprehensive", styles=UML_GRAPH) as g:
            # Class with spot, static, and abstract members
            shape = ClassNode(
                "Shape",
                spot="A",
                attributes=[
                    "{static} - count: int",
                    "# color: str",
                ],
                methods=[
                    "{abstract} + draw(): void",
                    "{static} + getCount(): int",
                ],
            )

            # Note attached to the class
            note = UMLNoteNode("Abstract base class for all shapes")
            shape >> note | UMLNoteEdge()

            dot = g.to_dot()
            # Verify all features are present
            self.assertIn("(A)", dot)  # Spot icon
            self.assertIn("<U>", dot)  # Static
            self.assertIn("<I>", dot)  # Abstract
            self.assertIn('shape="note"', dot)  # Note node
            self.assertIn('style="dashed"', dot)  # Note edge


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


class TestUMLSubgraphIntegration(unittest.TestCase):
    """Test UML diagram components integration with Subgraph and native features."""

    def test_uml_nodes_in_subgraph(self):
        """Test that UML nodes are correctly registered to subgraphs."""
        with Graph("test_uml_subgraph", styles=UML_GRAPH) as g:
            with Subgraph("package1") as s1:
                class1 = ClassNode(
                    "UserService",
                    attributes=["- users: List[User]"],
                    methods=["+ getUser(id: int): User"],
                )
                interface1 = InterfaceNode("IService", methods=["+ execute(): void"])

            dot = g.to_dot()
            # Verify subgraph exists
            self.assertIn('subgraph "cluster_package1"', dot)
            # Verify UML nodes are in the subgraph
            self.assertIn("UserService", dot)
            self.assertIn("IService", dot)
            self.assertIn("interface", dot)
            # Verify nodes are registered to subgraph (not top-level)
            self.assertEqual(len(s1._nodes), 2)
            self.assertIn("UserService", s1._nodes)
            self.assertIn("IService", s1._nodes)

    def test_multiple_uml_node_types_in_subgraph(self):
        """Test multiple UML node types in same subgraph."""
        with Graph("test_multi_types", styles=UML_GRAPH) as g:
            with Subgraph("domain_layer") as sub:
                abstract = AbstractClassNode(
                    "BaseEntity", attributes=["# id: int"], methods=["+ save(): void"]
                )
                concrete = ClassNode("User", attributes=["+ name: str"])
                iface = InterfaceNode("IRepository", methods=["+ findById(): Entity"])

            dot = g.to_dot()
            self.assertIn("BaseEntity", dot)
            self.assertIn("User", dot)
            self.assertIn("IRepository", dot)
            self.assertIn("abstract", dot)
            self.assertIn("interface", dot)
            self.assertEqual(len(sub._nodes), 3)

    def test_uml_edges_across_subgraphs(self):
        """Test UML edges connecting nodes in different subgraphs."""
        with Graph("test_cross_subgraph", styles=UML_GRAPH) as g:
            with Subgraph("domain") as s1:
                entity = ClassNode("Entity", attributes=["+ id: int"])

            with Subgraph("services") as s2:
                service = ClassNode(
                    "EntityService", methods=["+ getEntity(id): Entity"]
                )

            # Create edge across subgraphs
            service >> entity | DependencyEdge(label="uses")

            dot = g.to_dot()
            # Verify both subgraphs exist
            self.assertIn('subgraph "cluster_domain"', dot)
            self.assertIn('subgraph "cluster_services"', dot)
            # Verify edge exists
            self.assertIn('"EntityService" -> "Entity"', dot)
            self.assertIn('style="dashed"', dot)
            self.assertIn('label="uses"', dot)

    def test_inheritance_across_subgraphs(self):
        """Test inheritance relationships across subgraphs."""
        with Graph("test_inheritance_cross", styles=UML_GRAPH) as g:
            with Subgraph("base"):
                base = AbstractClassNode("Animal", methods=["+ speak(): void"])

            with Subgraph("derived"):
                dog = ClassNode("Dog", methods=["+ bark(): void"])
                cat = ClassNode("Cat", methods=["+ meow(): void"])

            dog >> base | InheritanceEdge()
            cat >> base | InheritanceEdge()

            dot = g.to_dot()
            self.assertIn('"Dog" -> "Animal"', dot)
            self.assertIn('"Cat" -> "Animal"', dot)
            self.assertIn('arrowhead="empty"', dot)

    def test_composition_in_subgraph(self):
        """Test composition relationships within subgraph."""
        with Graph("test_composition_subgraph", styles=UML_GRAPH) as g:
            with Subgraph("vehicle_package"):
                car = ClassNode("Car", attributes=["- engine: Engine"])
                engine = ClassNode("Engine", attributes=["+ power: int"])

                car >> engine | CompositionEdge(label="1")

            dot = g.to_dot()
            self.assertIn('"Car" -> "Engine"', dot)
            self.assertIn('arrowtail="diamond"', dot)
            self.assertIn('label="1"', dot)

    def test_nested_subgraphs_uml(self):
        """Test UML diagram with nested subgraph structure (package hierarchy)."""
        with Graph("test_nested_packages", styles=UML_GRAPH) as g:
            with Subgraph("backend") as s1:
                with Subgraph("models") as s2:
                    user = ClassNode("User", attributes=["+ name: str", "+ email: str"])
                    post = ClassNode("Post", attributes=["+ title: str"])

                with Subgraph("services") as s3:
                    user_service = ClassNode(
                        "UserService", methods=["+ createUser(): User"]
                    )

            # Create relationships
            user_service >> user | DependencyEdge()

            dot = g.to_dot()
            # Verify nested structure
            self.assertIn('subgraph "cluster_backend"', dot)
            self.assertIn('subgraph "cluster_models"', dot)
            self.assertIn('subgraph "cluster_services"', dot)
            # Verify nesting in object model
            self.assertEqual(len(g._subgraphs), 1)  # Only backend is top-level
            self.assertEqual(len(s1._subgraphs), 2)  # models and services are nested
            self.assertIn("User", s2._nodes)
            self.assertIn("UserService", s3._nodes)

    def test_uml_tuple_fanout(self):
        """Test UML nodes with tuple fan-out syntax."""
        with Graph("test_fanout", styles=UML_GRAPH) as g:
            base = AbstractClassNode("Shape", methods=["+ getArea(): float"])
            circle = ClassNode("Circle")
            square = ClassNode("Square")
            triangle = ClassNode("Triangle")

            # Fan-out: multiple derived classes inherit from base
            # Each derived class creates edge to base using >> operator
            circle >> base | InheritanceEdge()
            square >> base | InheritanceEdge()
            triangle >> base | InheritanceEdge()

            dot = g.to_dot()
            self.assertIn('"Circle" -> "Shape"', dot)
            self.assertIn('"Square" -> "Shape"', dot)
            self.assertIn('"Triangle" -> "Shape"', dot)
            # Verify all edges have inheritance styling
            self.assertEqual(dot.count('arrowhead="empty"'), 3)

    def test_uml_edge_chaining(self):
        """Test UML with edge chaining."""
        with Graph("test_chain", styles=UML_GRAPH) as g:
            a = ClassNode("A")
            b = ClassNode("B")
            c = ClassNode("C")

            # Chain multiple dependencies
            a >> b >> c | DependencyEdge()

            dot = g.to_dot()
            self.assertIn('"A" -> "B"', dot)
            self.assertIn('"B" -> "C"', dot)
            # Both edges should have dependency styling
            self.assertEqual(dot.count('style="dashed"'), 2)

    def test_uml_fanout_with_inheritance(self):
        """Test combining fan-out with different edge types."""
        with Graph("test_fanout_edges", styles=UML_GRAPH) as g:
            with Subgraph("interfaces"):
                drawable = InterfaceNode("Drawable", methods=["+ draw()"])

            with Subgraph("implementations"):
                shapes = [
                    ClassNode("Circle"),
                    ClassNode("Rectangle"),
                    ClassNode("Polygon"),
                ]

            # All shapes implement drawable
            for shape in shapes:
                shape >> drawable | ImplementsEdge()

            dot = g.to_dot()
            self.assertIn('"Circle" -> "Drawable"', dot)
            self.assertIn('"Rectangle" -> "Drawable"', dot)
            self.assertIn('"Polygon" -> "Drawable"', dot)
            # All should have dashed arrows (implements)
            self.assertEqual(dot.count('style="dashed"'), 3)

    def test_uml_subgraph_with_graph_styles(self):
        """Test UML_GRAPH style is applied correctly with subgraphs."""
        with Graph("test_graph_style", styles=UML_GRAPH) as g:
            with Subgraph("package1"):
                ClassNode("TestClass")

            dot = g.to_dot()
            # Verify UML_GRAPH styles are applied
            self.assertIn('rankdir="TB"', dot)
            self.assertIn('splines="ortho"', dot)

    def test_association_with_multiplicity_in_subgraph(self):
        """Test association edges with multiplicity labels in subgraphs."""
        with Graph("test_association", styles=UML_GRAPH) as g:
            with Subgraph("model"):
                student = ClassNode("Student", attributes=["+ name: str"])
                course = ClassNode("Course", attributes=["+ title: str"])

                student >> course | AssociationEdge(
                    label="enrolls in",
                    multiplicity_source="*",
                    multiplicity_target="*",
                )

            dot = g.to_dot()
            self.assertIn('"Student" -> "Course"', dot)
            self.assertIn('label="enrolls in"', dot)
            self.assertIn('taillabel="*"', dot)
            self.assertIn('headlabel="*"', dot)

    def test_aggregation_across_subgraphs(self):
        """Test aggregation relationships across subgraphs."""
        with Graph("test_aggregation_cross", styles=UML_GRAPH) as g:
            with Subgraph("organization"):
                dept = ClassNode("Department")

            with Subgraph("people"):
                employee = ClassNode("Employee")

            dept >> employee | AggregationEdge(label="0..*")

            dot = g.to_dot()
            self.assertIn('"Department" -> "Employee"', dot)
            self.assertIn('arrowtail="odiamond"', dot)
            self.assertIn('label="0..*"', dot)

    def test_uml_renders_with_subgraphs(self):
        """End-to-end test: verify graphviz can render UML with subgraphs."""
        with Graph("e2e_uml_subgraph", styles=UML_GRAPH) as g:
            with Subgraph("domain") as s1:
                base = AbstractClassNode("BaseEntity", methods=["+ save(): void"])
                user = ClassNode("User", attributes=["+ name: str"])
                post = ClassNode("Post", attributes=["+ title: str"])

                user >> base | InheritanceEdge()
                post >> base | InheritanceEdge()

            with Subgraph("services") as s2:
                service = InterfaceNode("IService", methods=["+ execute(): void"])
                user_service = ClassNode("UserService")

                user_service >> service | ImplementsEdge()
                user_service >> user | DependencyEdge()

            # This will raise if graphviz rejects the DOT
            svg = render_to_svg(g.to_dot())
            self.assertIn("<svg", svg)
            self.assertIn("BaseEntity", svg)
            self.assertIn("UserService", svg)

    def test_complex_uml_with_all_features(self):
        """Test complex UML diagram combining all features."""
        with Graph("complex_uml_complete", styles=UML_GRAPH) as g:
            # Multiple nested packages
            with Subgraph("application") as app:
                with Subgraph("domain") as domain:
                    entity = AbstractClassNode(
                        "Entity", attributes=["# id: int"], methods=["+ save(): void"]
                    )
                    user = ClassNode("User", attributes=["+ email: str"])
                    user >> entity | InheritanceEdge()

                with Subgraph("repository") as repo:
                    i_repo = InterfaceNode("IRepository", methods=["+ save(e: Entity)"])
                    user_repo = ClassNode("UserRepository")
                    user_repo >> i_repo | ImplementsEdge()
                    user_repo >> user | DependencyEdge()

                with Subgraph("service") as svc:
                    user_svc = ClassNode(
                        "UserService", methods=["+ createUser(data): User"]
                    )
                    user_svc >> user_repo | AggregationEdge()

            dot = g.to_dot()
            # Verify structure
            self.assertIn('subgraph "cluster_application"', dot)
            self.assertIn('subgraph "cluster_domain"', dot)
            self.assertIn('subgraph "cluster_repository"', dot)
            self.assertIn('subgraph "cluster_service"', dot)

            # Verify all relationships
            self.assertIn('"User" -> "Entity"', dot)
            self.assertIn('"UserRepository" -> "IRepository"', dot)
            self.assertIn('"UserRepository" -> "User"', dot)
            self.assertIn('"UserService" -> "UserRepository"', dot)

            # Verify it renders
            svg = render_to_svg(dot)
            self.assertIn("<svg", svg)


if __name__ == "__main__":
    unittest.main()
