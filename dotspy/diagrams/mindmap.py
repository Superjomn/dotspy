"""Mind map diagram components."""

from typing import Any, Dict, List, Optional, Union

from ..constants import FILLED, ROUNDED
from ..node import Node
from ..style import EdgeStyle, GraphStyle, NodeStyle
from .base import DiagramEdge, DiagramNode

# Mind map node styles
TOPIC_STYLE = NodeStyle(
    shape="ellipse",
    style=f"{FILLED},{ROUNDED}",
    fillcolor="lightblue",
    fontname="Helvetica-Bold",
    fontsize=16,
    penwidth=2.5,
)

BRANCH_STYLE = NodeStyle(
    shape="box",
    style=f"{FILLED},{ROUNDED}",
    fillcolor="lightgreen",
    fontname="Helvetica",
    fontsize=12,
    penwidth=1.5,
)

LEAF_STYLE = NodeStyle(
    shape="box",
    style=f"{FILLED},{ROUNDED}",
    fillcolor="lightyellow",
    fontname="Helvetica",
    fontsize=10,
    penwidth=1.0,
)


class TopicNode(DiagramNode):
    """
    Central topic node for mind maps.

    Represents the main idea or central concept with prominent styling.

    Example:
        >>> root = TopicNode("Project Ideas")
    """

    def __init__(
        self,
        label: str,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs,
    ):
        """
        Initialize a topic node.

        Args:
            label: Display label for the topic
            name: Unique identifier (uses label if not provided)
            styles: Additional NodeStyle objects to apply
            **attrs: Additional node attributes
        """
        # Use label as name if name not provided
        if name is None:
            name = label

        style_list = [TOPIC_STYLE]
        if styles:
            if isinstance(styles, list):
                style_list.extend(styles)
            else:
                style_list.append(styles)

        super().__init__(
            name=name,
            label=label,
            styles=style_list,
            **attrs,
        )


class BranchNode(DiagramNode):
    """
    Branch/subtopic node for mind maps.

    Represents main branches from the central topic.

    Example:
        >>> branch = BranchNode("Frontend")
    """

    def __init__(
        self,
        label: str,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs,
    ):
        """
        Initialize a branch node.

        Args:
            label: Display label for the branch
            name: Unique identifier (uses label if not provided)
            styles: Additional NodeStyle objects to apply
            **attrs: Additional node attributes
        """
        # Use label as name if name not provided
        if name is None:
            name = label

        style_list = [BRANCH_STYLE]
        if styles:
            if isinstance(styles, list):
                style_list.extend(styles)
            else:
                style_list.append(styles)

        super().__init__(
            name=name,
            label=label,
            styles=style_list,
            **attrs,
        )


class LeafNode(DiagramNode):
    """
    Leaf node for mind maps.

    Represents detail items at the end of branches.

    Example:
        >>> leaf = LeafNode("React")
    """

    def __init__(
        self,
        label: str,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs,
    ):
        """
        Initialize a leaf node.

        Args:
            label: Display label for the leaf
            name: Unique identifier (uses label if not provided)
            styles: Additional NodeStyle objects to apply
            **attrs: Additional node attributes
        """
        # Use label as name if name not provided
        if name is None:
            name = label

        style_list = [LEAF_STYLE]
        if styles:
            if isinstance(styles, list):
                style_list.extend(styles)
            else:
                style_list.append(styles)

        super().__init__(
            name=name,
            label=label,
            styles=style_list,
            **attrs,
        )


class BranchEdge(DiagramEdge):
    """
    Edge style for mind map connections.

    Uses bold lines with no arrows for a cleaner mind map look.

    Example:
        >>> root >> branch | BranchEdge()
    """

    def __init__(self, **attrs):
        edge_attrs = {
            "dir": "none",  # No arrows in mind maps
            "penwidth": 2.0,
            "color": "gray40",
        }
        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


# Mind map graph style preset
MINDMAP_GRAPH = GraphStyle(
    rankdir="LR",  # Left to right by default
    splines="curved",  # Curved edges for organic look
    nodesep=0.6,
    ranksep=1.2,
)


def mindmap(
    structure: Dict[str, Any],
    root_node: Optional[Node] = None,
    parent_is_topic: bool = True,
) -> Node:
    """
    Helper function to create a mind map from a nested dictionary structure.

    The dictionary structure represents the hierarchy:
    - Keys are node labels
    - Values can be:
        - Dict: Creates a branch node with nested children
        - List: Creates leaf nodes
        - None/empty: Creates a branch node with no children

    Args:
        structure: Nested dictionary representing the mind map hierarchy
        root_node: Optional parent node to attach to (used internally for recursion)
        parent_is_topic: Whether the parent is a topic node (affects child node types)

    Returns:
        The root node of the created mind map

    Example:
        >>> with Graph("ideas", styles=MINDMAP_GRAPH) as g:
        ...     mindmap({
        ...         "Project": {
        ...             "Frontend": ["React", "Vue", "Angular"],
        ...             "Backend": {
        ...                 "Python": ["Django", "Flask"],
        ...                 "Go": ["Gin", "Echo"]
        ...             },
        ...             "Database": ["PostgreSQL", "MongoDB"]
        ...         }
        ...     })
    """
    if not structure:
        return root_node

    # Get the root label (first key in dict)
    if isinstance(structure, dict):
        root_label = list(structure.keys())[0]
        children = structure[root_label]

        # Create root node if not provided
        if root_node is None:
            root_node = TopicNode(root_label)

        # Process children
        if isinstance(children, dict):
            # Children are branches
            for child_label, grandchildren in children.items():
                child_node = BranchNode(child_label)
                root_node >> child_node | BranchEdge()

                # Recursively process grandchildren
                if isinstance(grandchildren, dict):
                    mindmap(
                        {child_label: grandchildren},
                        root_node=child_node,
                        parent_is_topic=False,
                    )
                elif isinstance(grandchildren, list):
                    # Create leaf nodes
                    for leaf_label in grandchildren:
                        leaf_node = LeafNode(leaf_label)
                        child_node >> leaf_node | BranchEdge()

        elif isinstance(children, list):
            # Children are leaves directly under topic
            for child_label in children:
                if parent_is_topic:
                    child_node = BranchNode(child_label)
                else:
                    child_node = LeafNode(child_label)
                root_node >> child_node | BranchEdge()

        return root_node

    return root_node


def radial_mindmap(
    structure: Dict[str, Any],
    root_node: Optional[Node] = None,
) -> Node:
    """
    Create a radial mind map (topic in center, branches radiating out).

    This is a convenience wrapper around mindmap() with a radial graph style.
    Use this with RADIAL_MINDMAP_GRAPH style.

    Args:
        structure: Nested dictionary representing the mind map hierarchy
        root_node: Optional parent node to attach to

    Returns:
        The root node of the created mind map

    Example:
        >>> with Graph("radial", styles=RADIAL_MINDMAP_GRAPH) as g:
        ...     radial_mindmap({
        ...         "Central Idea": {
        ...             "Branch 1": ["Item A", "Item B"],
        ...             "Branch 2": ["Item C", "Item D"]
        ...         }
        ...     })
    """
    return mindmap(structure, root_node=root_node, parent_is_topic=True)


# Alternative radial layout style
RADIAL_MINDMAP_GRAPH = GraphStyle(
    layout="twopi",  # Radial layout engine
    splines="curved",
    ranksep=2.0,
    nodesep=1.0,
)
