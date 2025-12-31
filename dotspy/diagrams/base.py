"""Base classes and utilities for diagram-specific nodes and edges."""

from typing import Any, Dict, List, Optional, Union

from ..node import Node
from ..style import EdgeStyle, NodeStyle


class DiagramNode(Node):
    """
    Base class for diagram-specific nodes.

    Provides common functionality for specialized diagram nodes like
    UML classes, mind map topics, etc.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs,
    ):
        super().__init__(name=name, styles=styles, **attrs)


class DiagramEdge:
    """
    Base class for diagram-specific edges.

    This is a style template that can be applied to existing edges
    using the | operator. It doesn't inherit from Edge because it's
    meant to be used as a style applicator, not as an edge itself.
    """

    def __init__(
        self,
        styles: Optional[Union[EdgeStyle, List[EdgeStyle]]] = None,
        **attrs,
    ):
        """
        Initialize an edge style template.

        Args:
            styles: EdgeStyle or list of EdgeStyles to apply
            **attrs: Additional edge attributes
        """
        self._template_styles = styles
        self._template_attrs = attrs

    def to_style(self) -> EdgeStyle:
        """
        Convert this diagram edge to an EdgeStyle object.

        Returns:
            EdgeStyle with all attributes from this diagram edge
        """
        # Merge styles if provided
        if self._template_styles:
            if isinstance(self._template_styles, list):
                # Merge multiple styles
                merged = {}
                for style in self._template_styles:
                    merged.update(style.to_dict())
                merged.update(self._template_attrs)
                return EdgeStyle(**merged)
            else:
                # Single style - merge with attrs
                merged = self._template_styles.to_dict()
                merged.update(self._template_attrs)
                return EdgeStyle(**merged)
        else:
            # No styles, just attrs
            return EdgeStyle(**self._template_attrs)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this diagram edge to a dictionary.

        Returns:
            Dictionary with all edge attributes
        """
        return self.to_style().to_dict()


def create_table_html(
    title: str,
    sections: List[Dict[str, Any]],
    border: int = 0,
    cellborder: int = 1,
    cellspacing: int = 0,
    cellpadding: int = 4,
) -> str:
    """
    Create an HTML table for use in node labels (e.g., UML class diagrams).

    Args:
        title: Title text (e.g., class name)
        sections: List of section dicts with 'rows' key containing list of strings
        border: Table border width
        cellborder: Cell border width
        cellspacing: Cell spacing
        cellpadding: Cell padding

    Returns:
        HTML string suitable for DOT HTML labels

    Example:
        >>> html = create_table_html(
        ...     "MyClass",
        ...     [
        ...         {"rows": ["+ name: str", "- age: int"]},
        ...         {"rows": ["+ speak(): void"]}
        ...     ]
        ... )
    """
    lines = [
        f'<TABLE BORDER="{border}" CELLBORDER="{cellborder}" '
        f'CELLSPACING="{cellspacing}" CELLPADDING="{cellpadding}">'
    ]

    # Title row
    lines.append(f"  <TR><TD><B>{title}</B></TD></TR>")

    # Section rows
    for section in sections:
        if section.get("rows"):
            for row in section["rows"]:
                align = section.get("align", "LEFT")
                lines.append(f'  <TR><TD ALIGN="{align}">{row}</TD></TR>')

    lines.append("</TABLE>")
    return "\n".join(lines)


def escape_html(text: str) -> str:
    """
    Escape special characters for HTML labels in DOT format.

    Args:
        text: Text to escape

    Returns:
        Escaped text safe for HTML labels
    """
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&apos;",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text
