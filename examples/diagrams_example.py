"""Examples demonstrating the diagrams module."""

from dotspy import Graph
from dotspy.diagrams import (
    MINDMAP_GRAPH,
    UML_GRAPH,
    AggregationEdge,
    AssociationEdge,
    BranchNode,
    ClassNode,
    CompositionEdge,
    ImplementsEdge,
    InheritanceEdge,
    InterfaceNode,
    LeafNode,
    TopicNode,
    mindmap,
)


def uml_example():
    """Create a UML class diagram example."""
    print("Creating UML class diagram...")

    with Graph("uml_example", styles=UML_GRAPH) as g:
        # Define interfaces
        drawable = InterfaceNode("Drawable", methods=["+ draw(): void"])

        # Define abstract class
        shape = ClassNode(
            "Shape",
            attributes=["# color: str", "# filled: bool"],
            methods=["+ getArea(): float", "+ getPerimeter(): float"],
        )

        # Define concrete classes
        circle = ClassNode(
            "Circle",
            attributes=["- radius: float"],
            methods=["+ getArea(): float", "+ draw(): void"],
        )

        rectangle = ClassNode(
            "Rectangle",
            attributes=["- width: float", "- height: float"],
            methods=["+ getArea(): float", "+ draw(): void"],
        )

        # Relationships
        circle >> shape | InheritanceEdge()
        rectangle >> shape | InheritanceEdge()
        circle >> drawable | ImplementsEdge()
        rectangle >> drawable | ImplementsEdge()

        g.render("uml_example.png")
        print("UML diagram saved to uml_example.png")
        print(g.to_dot())


def composition_example():
    """Create a UML diagram showing composition and aggregation."""
    print("\nCreating composition/aggregation example...")

    with Graph("composition_example", styles=UML_GRAPH) as g:
        car = ClassNode("Car", attributes=["- model: str"])
        engine = ClassNode("Engine", attributes=["- horsepower: int"])
        wheel = ClassNode("Wheel", attributes=["- diameter: float"])
        driver = ClassNode("Driver", attributes=["- name: str"])

        # Composition (car owns engine)
        car >> engine | CompositionEdge(label="has")

        # Aggregation (car uses wheels, but wheels can exist independently)
        car >> wheel | AggregationEdge(label="has 4")

        # Association (car associated with driver)
        car >> driver | AssociationEdge(
            label="driven by", multiplicity_source="1", multiplicity_target="1"
        )

        g.render("composition_example.png")
        print("Composition diagram saved to composition_example.png")


def mindmap_manual_example():
    """Create a mind map manually."""
    print("\nCreating manual mind map...")

    with Graph("mindmap_manual", styles=MINDMAP_GRAPH) as g:
        # Central topic
        project = TopicNode("Software Project")

        # Main branches
        frontend = BranchNode("Frontend")
        backend = BranchNode("Backend")
        devops = BranchNode("DevOps")

        # Connect branches to topic
        from dotspy.diagrams import BranchEdge

        project >> frontend | BranchEdge()
        project >> backend | BranchEdge()
        project >> devops | BranchEdge()

        # Add leaves
        react = LeafNode("React")
        vue = LeafNode("Vue")
        python = LeafNode("Python")
        go = LeafNode("Go")
        docker = LeafNode("Docker")
        k8s = LeafNode("Kubernetes")

        frontend >> react | BranchEdge()
        frontend >> vue | BranchEdge()
        backend >> python | BranchEdge()
        backend >> go | BranchEdge()
        devops >> docker | BranchEdge()
        devops >> k8s | BranchEdge()

        g.render("mindmap_manual.png")
        print("Manual mind map saved to mindmap_manual.png")


def mindmap_helper_example():
    """Create a mind map using the helper function."""
    print("\nCreating mind map with helper function...")

    with Graph("mindmap_helper", styles=MINDMAP_GRAPH) as g:
        mindmap(
            {
                "Learning Plan": {
                    "Programming Languages": {
                        "Python": ["Django", "FastAPI", "Data Science"],
                        "JavaScript": ["React", "Node.js", "TypeScript"],
                        "Go": ["Concurrency", "Microservices"],
                    },
                    "Databases": {
                        "SQL": ["PostgreSQL", "MySQL"],
                        "NoSQL": ["MongoDB", "Redis"],
                    },
                    "DevOps": ["Docker", "Kubernetes", "CI/CD", "Terraform"],
                }
            }
        )

        g.render("mindmap_helper.png")
        print("Helper mind map saved to mindmap_helper.png")


if __name__ == "__main__":
    uml_example()
    composition_example()
    mindmap_manual_example()
    mindmap_helper_example()
    print("\n✓ All examples completed successfully!")
