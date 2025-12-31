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
            **attrs: Additional node attributes
        """
        # Build sections for the table
        sections = []

        # Attributes section
        if attributes:
            sections.append(
                {"rows": [escape_html(attr) for attr in attributes], "align": "LEFT"}
            )

        # Methods section
        if methods:
            sections.append(
                {"rows": [escape_html(method) for method in methods], "align": "LEFT"}
            )

        # Add stereotype to title if provided
        title = escape_html(class_name)
        if stereotype:
            title = f"&lt;&lt;{escape_html(stereotype)}&gt;&gt;<BR/>{title}"

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
        **attrs,
    ):
        """
        Initialize a UML interface node.

        Args:
            interface_name: Name of the interface
            methods: List of method strings
            styles: Additional NodeStyle objects to apply
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
        **attrs,
    ):
        """
        Initialize a UML abstract class node.

        Args:
            class_name: Name of the abstract class
            attributes: List of attribute strings
            methods: List of method strings
            styles: Additional NodeStyle objects to apply
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


# UML Graph Style Preset
UML_GRAPH = GraphStyle(
    rankdir="TB",
    splines="ortho",  # Orthogonal routing for cleaner UML diagrams
    nodesep=0.8,
    ranksep=1.0,
)
