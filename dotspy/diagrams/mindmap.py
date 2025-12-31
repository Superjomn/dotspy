"""Mind map diagram components."""

from typing import List, Optional, Union

from ..constants import DASHED, FILLED, ROUNDED
from ..style import EdgeStyle, GraphStyle, NodeStyle
from .base import DiagramEdge, DiagramNode

# Mind map node style presets
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

# Default style for MindNode (neutral, can be customized)
DEFAULT_MIND_STYLE = NodeStyle(
    shape="box",
    style=f"{FILLED},{ROUNDED}",
    fillcolor="lightblue",
    fontname="Helvetica",
    fontsize=12,
    penwidth=1.5,
)

NOTE_STYLE = NodeStyle(
    shape="note",
    style=f"{FILLED}",
    fillcolor="lightyellow",
    fontname="Helvetica",
    fontsize=10,
    color="gray",
)


class MindNode(DiagramNode):
    """
    Unified node for mind maps.

    Represents any node in a mind map structure. Users can optionally apply
    preset styles (TOPIC_STYLE, BRANCH_STYLE, LEAF_STYLE) or use custom styling.

    Example:
        >>> root = MindNode("Project Ideas")
        >>> root = MindNode("Project Ideas", styles=TOPIC_STYLE)
        >>> branch = MindNode("Frontend", styles=BRANCH_STYLE)
        >>> leaf = MindNode("React", styles=LEAF_STYLE)
    """

    def __init__(
        self,
        label: str,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs,
    ):
        """
        Initialize a mind map node.

        Args:
            label: Display label for the node
            name: Unique identifier (uses label if not provided)
            styles: NodeStyle objects to apply (defaults to DEFAULT_MIND_STYLE)
            **attrs: Additional node attributes
        """
        # Use label as name if name not provided
        if name is None:
            name = label

        # Apply default style if no styles provided
        if styles is None:
            style_list = [DEFAULT_MIND_STYLE]
        else:
            style_list = [DEFAULT_MIND_STYLE]
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


class NoteNode(DiagramNode):
    """
    Annotation/note node for mind maps.

    Represents a note or comment that can be attached to other nodes.
    Uses a note shape with subtle styling. When used as a target with >>,
    NoteEdge styling is automatically applied.

    Example:
        >>> note = NoteNode("This is important!")
        >>> some_node >> note  # Automatically applies NoteEdge styling
    """

    # Marker attribute to identify NoteNode for auto-styling
    _is_note_node = True

    def __init__(
        self,
        label: str,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs,
    ):
        """
        Initialize a note node.

        Args:
            label: Display label for the note
            name: Unique identifier (uses label if not provided)
            styles: Additional NodeStyle objects to apply
            **attrs: Additional node attributes
        """
        # Use label as name if name not provided
        if name is None:
            name = f"note_{label}"

        style_list = [NOTE_STYLE]
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


class NoteEdge(DiagramEdge):
    """
    Edge style for connecting notes to nodes.

    Uses dashed lines with no arrows for a subtle connection.

    Example:
        >>> node >> note | NoteEdge()
    """

    def __init__(self, **attrs):
        edge_attrs = {
            "dir": "none",  # No arrows for notes
            "style": DASHED,
            "penwidth": 1.0,
            "color": "gray60",
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

# Alternative radial layout style
RADIAL_MINDMAP_GRAPH = GraphStyle(
    layout="twopi",  # Radial layout engine
    splines="curved",
    ranksep=2.0,
    nodesep=1.0,
)


# Backward compatibility aliases (deprecated)
# Users should use MindNode with style presets instead
TopicNode = MindNode
BranchNode = MindNode
LeafNode = MindNode
