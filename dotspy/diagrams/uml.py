"""UML class diagram components."""

from typing import List, Optional, Union

from ..constants import DASHED, FILLED, NORMAL
from ..node import HTMLNode
from ..style import EdgeStyle, GraphStyle, NodeStyle
from .base import DiagramEdge, DiagramNode, create_table_html, escape_html

# UML-specific node styles
UML_CLASS_STYLE = NodeStyle(
    shape="box",
    style=FILLED,
    fillcolor="lightblue",
    fontname="Helvetica",
)

UML_INTERFACE_STYLE = NodeStyle(
    shape="box",
    style=FILLED,
    fillcolor="lightyellow",
    fontname="Helvetica-Oblique",
)

UML_ABSTRACT_STYLE = NodeStyle(
    shape="box",
    style=FILLED,
    fillcolor="lightgray",
    fontname="Helvetica-Oblique",
)

UML_NOTE_STYLE = NodeStyle(
    shape="note",
    style=FILLED,
    fillcolor="lightyellow",
    fontname="Helvetica",
    fontsize=10,
)

# Spot icon colors (PlantUML-style class indicators)
SPOT_COLORS = {
    "C": "lightblue",  # Class (default)
    "I": "lightyellow",  # Interface
    "A": "lightgray",  # Abstract
    "E": "lightgreen",  # Enum
}


def wrap_text(text: str, width: int = 60, indent: str = "&nbsp;&nbsp;") -> str:
    """
    Wrap text to specified width, preserving structure for UML attributes/methods.
    Splits primarily on commas (for parameter lists) and spaces.
    """
    if len(text) <= width:
        return escape_html(text)

    lines = []
    remaining = text

    while len(remaining) > width:
        # Find best split point
        # Priority: 1. Comma (args), 2. Space, 3. Hard split

        limit = width
        split_idx = -1

        # Check for comma
        last_comma = remaining.rfind(",", 0, limit)
        if last_comma != -1:
            split_idx = last_comma + 1  # Include comma
        else:
            # Check for space
            last_space = remaining.rfind(" ", 0, limit)
            if last_space != -1:
                split_idx = last_space

        if split_idx == -1:
            split_idx = limit  # Hard split

        chunk = remaining[:split_idx]
        lines.append(escape_html(chunk))

        remaining = remaining[split_idx:].lstrip()

    if remaining:
        lines.append(escape_html(remaining))

    # Indent all lines except the first
    if not lines:
        return ""

    result = lines[0]
    for line in lines[1:]:
        result += f"<BR ALIGN='LEFT'/>{indent}{line}"

    return result


def format_member(text: str, width: int = 60, indent: str = "&nbsp;&nbsp;") -> str:
    """
    Format a class member with modifier support and wrapping.

    Supports modifiers:
        {static} - Underline the member (e.g., "{static} count: int")
        {abstract} - Italicize the member (e.g., "{abstract} + draw(): void")

    Args:
        text: Member text with optional modifier prefix
        width: Maximum width before wrapping
        indent: Indentation for wrapped lines

    Returns:
        HTML-formatted and wrapped member text
    """
    is_static = text.startswith("{static}")
    is_abstract = text.startswith("{abstract}")

    # Strip modifier prefix
    clean_text = text.replace("{static}", "").replace("{abstract}", "").strip()
    wrapped = wrap_text(clean_text, width, indent)

    # Apply HTML formatting
    if is_static:
        return f"<U>{wrapped}</U>"
    elif is_abstract:
        return f"<I>{wrapped}</I>"
    return wrapped


class ClassNode(HTMLNode, DiagramNode):
    """
    UML class node with compartments for attributes and methods.

    Creates a table-based HTML label with:
    - Class name (bold, top compartment)
    - Attributes (middle compartment)
    - Methods (bottom compartment)

    Example:
        >>> animal = ClassNode(
        ...     "Animal",
        ...     attributes=["+ name: str", "- age: int"],
        ...     methods=["+ speak(): void", "+ move(): void"]
        ... )
    """

    def __init__(
        self,
        class_name: str,
        attributes: Optional[List[str]] = None,
        methods: Optional[List[str]] = None,
        stereotype: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        wrap_width: int = 60,
        spot: Optional[str] = None,
        spot_color: Optional[str] = None,
        **attrs,
    ):
        """
        Initialize a UML class node.

        Args:
            class_name: Name of the class
            attributes: List of attribute strings (e.g., "+ name: str")
            methods: List of method strings (e.g., "+ getName(): str")
            stereotype: Optional stereotype (e.g., "<<interface>>", "<<abstract>>")
            styles: Additional NodeStyle objects to apply
            wrap_width: Maximum width of text before wrapping (default: 60)
            spot: Optional spot character (e.g., "C", "I", "A", "E") for class indicator
            spot_color: Optional color for spot (overrides default SPOT_COLORS)
            **attrs: Additional node attributes
        """
        # Build sections for the table
        sections = []

        # Attributes section
        if attributes:
            sections.append(
                {
                    "rows": [
                        format_member(attr, width=wrap_width) for attr in attributes
                    ],
                    "align": "LEFT",
                }
            )

        # Methods section
        if methods:
            sections.append(
                {
                    "rows": [
                        format_member(method, width=wrap_width) for method in methods
                    ],
                    "align": "LEFT",
                }
            )

        # Add stereotype to title if provided
        title = escape_html(class_name)
        if stereotype:
            title = f"&lt;&lt;{escape_html(stereotype)}&gt;&gt;<BR/>{title}"

        # Add spot icon if provided (simple text-based approach)
        if spot:
            spot_bg = spot_color or SPOT_COLORS.get(spot, "lightgray")
            # Use a simple circle character with colored background via FONT tag
            # Format: (X) prefix where X is the spot letter
            title = f"<FONT COLOR='white' BGCOLOR='{spot_bg}'>({escape_html(spot)})</FONT> {title}"

        # Create HTML table
        html_content = create_table_html(title, sections)

        # Merge with default UML class style
        style_list = [UML_CLASS_STYLE]
        if styles:
            if isinstance(styles, list):
                style_list.extend(styles)
            else:
                style_list.append(styles)

        # Initialize as HTMLNode
        super().__init__(
            name=class_name,
            html=html_content,
            styles=style_list,
            **attrs,
        )


class InterfaceNode(ClassNode):
    """
    UML interface node (class with <<interface>> stereotype).

    Example:
        >>> drawable = InterfaceNode(
        ...     "Drawable",
        ...     methods=["+ draw(): void"]
        ... )
    """

    def __init__(
        self,
        interface_name: str,
        methods: Optional[List[str]] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        wrap_width: int = 60,
        **attrs,
    ):
        """
        Initialize a UML interface node.

        Args:
            interface_name: Name of the interface
            methods: List of method strings
            styles: Additional NodeStyle objects to apply
            wrap_width: Maximum width of text before wrapping (default: 60)
            **attrs: Additional node attributes
        """
        style_list = [UML_INTERFACE_STYLE]
        if styles:
            if isinstance(styles, list):
                style_list.extend(styles)
            else:
                style_list.append(styles)

        super().__init__(
            class_name=interface_name,
            attributes=None,
            methods=methods,
            stereotype="interface",
            styles=style_list,
            wrap_width=wrap_width,
            **attrs,
        )


class AbstractClassNode(ClassNode):
    """
    UML abstract class node.

    Example:
        >>> shape = AbstractClassNode(
        ...     "Shape",
        ...     methods=["+ getArea(): float"]
        ... )
    """

    def __init__(
        self,
        class_name: str,
        attributes: Optional[List[str]] = None,
        methods: Optional[List[str]] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        wrap_width: int = 60,
        **attrs,
    ):
        """
        Initialize a UML abstract class node.

        Args:
            class_name: Name of the abstract class
            attributes: List of attribute strings
            methods: List of method strings
            styles: Additional NodeStyle objects to apply
            wrap_width: Maximum width of text before wrapping (default: 60)
            **attrs: Additional node attributes
        """
        style_list = [UML_ABSTRACT_STYLE]
        if styles:
            if isinstance(styles, list):
                style_list.extend(styles)
            else:
                style_list.append(styles)

        super().__init__(
            class_name=class_name,
            attributes=attributes,
            methods=methods,
            stereotype="abstract",
            styles=style_list,
            wrap_width=wrap_width,
            **attrs,
        )


class UMLNoteNode(DiagramNode):
    """
    UML note for documenting classes and relationships.

    Represents a note or comment that can be attached to UML elements.
    Uses a note shape with yellow background. When used as a target with >>,
    UMLNoteEdge styling can be applied.

    Example:
        >>> note = UMLNoteNode("This class handles authentication")
        >>> user_class >> note | UMLNoteEdge()
    """

    # Marker attribute to identify UMLNoteNode for auto-styling
    _is_note_node = True

    def __init__(
        self,
        text: str,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs,
    ):
        """
        Initialize a UML note node.

        Args:
            text: Note text content
            name: Unique identifier (uses text if not provided)
            styles: Additional NodeStyle objects to apply
            **attrs: Additional node attributes
        """
        # Use text as name if name not provided
        if name is None:
            name = f"note_{text[:20]}"  # Use first 20 chars for unique name

        style_list = [UML_NOTE_STYLE]
        if styles:
            if isinstance(styles, list):
                style_list.extend(styles)
            else:
                style_list.append(styles)

        super().__init__(
            name=name,
            label=text,
            styles=style_list,
            **attrs,
        )


# UML Edge Types


class InheritanceEdge(DiagramEdge):
    """
    UML inheritance/generalization edge (hollow arrow).

    Represents "extends" or "is-a" relationship.

    Example:
        >>> dog >> animal | InheritanceEdge()
    """

    def __init__(self, **attrs):
        edge_attrs = {
            "arrowhead": "empty",
            "color": "black",
            "penwidth": 1.5,
        }
        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


class ImplementsEdge(DiagramEdge):
    """
    UML realization/implementation edge (dashed hollow arrow).

    Represents "implements" relationship (class to interface).

    Example:
        >>> dog >> animal_interface | ImplementsEdge()
    """

    def __init__(self, **attrs):
        edge_attrs = {
            "arrowhead": "empty",
            "style": DASHED,
            "color": "black",
            "penwidth": 1.5,
        }
        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


class CompositionEdge(DiagramEdge):
    """
    UML composition edge (filled diamond).

    Represents strong "has-a" relationship with lifecycle dependency.

    Example:
        >>> car >> engine | CompositionEdge()
    """

    def __init__(self, label: Optional[str] = None, **attrs):
        edge_attrs = {
            "arrowhead": NORMAL,
            "arrowtail": "diamond",
            "dir": "both",
            "color": "black",
            "penwidth": 1.5,
        }
        if label:
            edge_attrs["label"] = label
        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


class AggregationEdge(DiagramEdge):
    """
    UML aggregation edge (hollow diamond).

    Represents weak "has-a" relationship without lifecycle dependency.

    Example:
        >>> department >> employee | AggregationEdge()
    """

    def __init__(self, label: Optional[str] = None, **attrs):
        edge_attrs = {
            "arrowhead": NORMAL,
            "arrowtail": "odiamond",
            "dir": "both",
            "color": "black",
            "penwidth": 1.5,
        }
        if label:
            edge_attrs["label"] = label
        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


class AssociationEdge(DiagramEdge):
    """
    UML association edge (simple line with optional arrow).

    Represents a general relationship between classes.

    Example:
        >>> student >> course | AssociationEdge(label="enrolls in")
    """

    def __init__(
        self,
        label: Optional[str] = None,
        multiplicity_source: Optional[str] = None,
        multiplicity_target: Optional[str] = None,
        bidirectional: bool = False,
        **attrs,
    ):
        edge_attrs = {
            "color": "black",
            "penwidth": 1.5,
        }

        if label:
            edge_attrs["label"] = label

        if bidirectional:
            edge_attrs["dir"] = "none"
        else:
            edge_attrs["arrowhead"] = NORMAL

        # Add multiplicity as head/tail labels
        if multiplicity_source:
            edge_attrs["taillabel"] = multiplicity_source
        if multiplicity_target:
            edge_attrs["headlabel"] = multiplicity_target

        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


class DependencyEdge(DiagramEdge):
    """
    UML dependency edge (dashed arrow).

    Represents "uses" or "depends on" relationship.

    Example:
        >>> client >> service | DependencyEdge()
    """

    def __init__(self, label: Optional[str] = None, **attrs):
        edge_attrs = {
            "arrowhead": "vee",
            "style": DASHED,
            "color": "gray",
            "penwidth": 1.0,
        }
        if label:
            edge_attrs["label"] = label
        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


class UMLNoteEdge(DiagramEdge):
    """
    UML note edge (dashed line for connecting notes).

    Represents an attachment between a UML note and a class or relationship.
    Uses a dashed line with no arrow for a subtle connection.

    Example:
        >>> class_node >> note | UMLNoteEdge()
    """

    def __init__(self, **attrs):
        edge_attrs = {
            "dir": "none",  # No arrows for note connections
            "style": DASHED,
            "penwidth": 1.0,
            "color": "gray60",
        }
        edge_attrs.update(attrs)
        style = EdgeStyle(**edge_attrs)
        super().__init__(styles=style)


# UML Graph Style Preset
UML_GRAPH = GraphStyle(
    rankdir="TB",
    splines="ortho",  # Orthogonal routing for cleaner UML diagrams
    nodesep=0.8,
    ranksep=1.0,
)
