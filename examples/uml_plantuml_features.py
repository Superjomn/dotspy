"""
Example demonstrating PlantUML-style features in dotspy UML diagrams.

This example showcases:
1. UML Notes - documentation notes attached to classes
2. Static/Abstract member formatting - {static} and {abstract} modifiers
3. Spot icons - colored circle indicators on class headers
"""

from dotspy import Graph
from dotspy.diagrams import (
    UML_GRAPH,
    AbstractClassNode,
    ClassNode,
    ImplementsEdge,
    InheritanceEdge,
    InterfaceNode,
    UMLNoteEdge,
    UMLNoteNode,
)


def main():
    """Create a UML diagram showcasing PlantUML-style features."""

    with Graph("plantuml_features_demo", styles=UML_GRAPH) as g:
        # Interface with spot icon
        drawable = InterfaceNode(
            "Drawable",
            methods=["+ draw(): void"],
        )

        # Abstract class with abstract methods and spot icon
        shape = AbstractClassNode(
            "Shape",
            attributes=[
                "{static} - shapeCount: int",
                "# color: str",
                "# filled: bool",
            ],
            methods=[
                "{abstract} + getArea(): float",
                "{abstract} + getPerimeter(): float",
                "{static} + getShapeCount(): int",
            ],
        )

        # Concrete class with static members and spot icon
        circle = ClassNode(
            "Circle",
            spot="C",
            attributes=[
                "{static} - PI: float = 3.14159",
                "- radius: float",
            ],
            methods=[
                "+ Circle(radius: float)",
                "+ getArea(): float",
                "+ getPerimeter(): float",
                "+ draw(): void",
            ],
        )

        # Another concrete class
        rectangle = ClassNode(
            "Rectangle",
            spot="C",
            attributes=[
                "- width: float",
                "- height: float",
            ],
            methods=[
                "+ Rectangle(w: float, h: float)",
                "+ getArea(): float",
                "+ getPerimeter(): float",
                "+ draw(): void",
            ],
        )

        # Singleton pattern example with static members
        singleton = ClassNode(
            "ShapeFactory",
            spot="C",
            attributes=[
                "{static} - instance: ShapeFactory",
            ],
            methods=[
                "{static} + getInstance(): ShapeFactory",
                "+ createCircle(radius: float): Circle",
                "+ createRectangle(w: float, h: float): Rectangle",
            ],
        )

        # UML Notes for documentation
        note_shape = UMLNoteNode(
            "Abstract base class for all geometric shapes.\n"
            "Maintains a count of all shape instances."
        )

        note_singleton = UMLNoteNode(
            "Singleton pattern ensures only one\n" "factory instance exists."
        )

        note_pi = UMLNoteNode("Mathematical constant π")

        # Relationships
        circle >> shape | InheritanceEdge()
        rectangle >> shape | InheritanceEdge()
        circle >> drawable | ImplementsEdge()
        rectangle >> drawable | ImplementsEdge()

        # Attach notes
        shape >> note_shape | UMLNoteEdge()
        singleton >> note_singleton | UMLNoteEdge()
        circle >> note_pi | UMLNoteEdge()

        # Render the diagram
        g.render("uml_plantuml_features.png")
        print("✓ UML diagram with PlantUML features saved to uml_plantuml_features.png")

        # Also print the DOT source
        print("\nGenerated DOT source:")
        print(g.to_dot())


if __name__ == "__main__":
    main()
