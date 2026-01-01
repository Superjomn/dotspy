"""
Diagrams module for dotspy.

Provides specialized node and edge types for common diagram scenarios:
- UML class diagrams
- Mind maps
- And more to come...
"""

from .base import DiagramEdge, DiagramNode, create_table_html, escape_html
from .mindmap import (
    MINDMAP_GRAPH,
    RADIAL_MINDMAP_GRAPH,
    BranchEdge,
    BranchNode,
    LeafNode,
    MindNode,
    NoteEdge,
    NoteNode,
    TopicNode,
)
from .plantuml_parser import create_node
from .uml import (
    UML_GRAPH,
    AbstractClassNode,
    AggregationEdge,
    AssociationEdge,
    ClassNode,
    CompositionEdge,
    DependencyEdge,
    ImplementsEdge,
    InheritanceEdge,
    InterfaceNode,
    UMLNoteEdge,
    UMLNoteNode,
)

__all__ = [
    # Base classes
    "DiagramNode",
    "DiagramEdge",
    "create_table_html",
    "escape_html",
    # UML components
    "ClassNode",
    "InterfaceNode",
    "AbstractClassNode",
    "UMLNoteNode",
    "InheritanceEdge",
    "ImplementsEdge",
    "CompositionEdge",
    "AggregationEdge",
    "AssociationEdge",
    "DependencyEdge",
    "UMLNoteEdge",
    "UML_GRAPH",
    "create_node",
    # Mind map components
    "MindNode",
    "NoteNode",
    "NoteEdge",
    "TopicNode",  # Backward compatibility alias
    "BranchNode",  # Backward compatibility alias
    "LeafNode",  # Backward compatibility alias
    "BranchEdge",
    "MINDMAP_GRAPH",
    "RADIAL_MINDMAP_GRAPH",
]
