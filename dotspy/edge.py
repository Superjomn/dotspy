from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic import ConfigDict, Field, PrivateAttr

from .attributes import EdgeAttributes
from .context import get_active_edge_styles, get_current_graph, get_graph
from .style import EdgeStyle, merge_styles

if TYPE_CHECKING:
    from .node import Node


class Edge(EdgeAttributes):
    """Represents an edge between two nodes."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    # Use strings for forward references to avoid circular import issues in Pydantic
    source: Any = Field(..., description="Source node.")
    target: Any = Field(..., description="Target node.")

    # Internal state
    _attrs: Dict[str, Any] = PrivateAttr(default_factory=dict)

    def __init__(
        self,
        source: "Node",
        target: "Node",
        styles: Optional[Union[EdgeStyle, List[EdgeStyle]]] = None,
        **attrs,
    ):
        # Resolve attributes from context and arguments
        context_attrs = {}
        for ctx_style in get_active_edge_styles():
            context_attrs.update(ctx_style.to_dict())

        style_attrs = merge_styles(styles)

        # Auto-apply NoteEdge styling if target is a NoteNode
        if hasattr(target, "_is_note_node") and target._is_note_node:
            # Import here to avoid circular import
            from .diagrams.mindmap import NoteEdge

            note_edge = NoteEdge()
            note_style = note_edge.to_style().to_dict()
            # NoteEdge styling takes precedence over context but not explicit styles
            combined_attrs = {**context_attrs, **note_style, **style_attrs, **attrs}
        else:
            combined_attrs = {**context_attrs, **style_attrs, **attrs}

        super().__init__(source=source, target=target, **combined_attrs)

        # Register with current graph
        self._register()

    def _register(self):
        graph = get_current_graph() or get_graph()
        if graph:
            graph._add_edge(self)

    def __call__(
        self, styles: Optional[Union[EdgeStyle, List[EdgeStyle]]] = None, **attrs
    ) -> "Edge":
        """Update attributes: (node1 >> node2)(color="red")"""
        updates = merge_styles(styles)
        updates.update(attrs)

        # Update model fields dynamically
        for k, v in updates.items():
            setattr(self, k, v)

        return self

    def __or__(
        self, styles: Union[EdgeStyle, List[EdgeStyle], Dict[str, Any]]
    ) -> "Edge":
        """Apply style: (node1 >> node2) | my_style"""
        # Check if it's a DiagramEdge or similar object with to_style() method
        if hasattr(styles, "to_style"):
            styles = styles.to_style()

        if isinstance(styles, dict):
            self(**styles)
        else:
            self(styles=styles)
        return self

    def __getitem__(self, styles: Union[EdgeStyle, List[EdgeStyle]]) -> "Edge":
        """Apply style: (node1 >> node2)[my_style]"""
        return self(styles=styles)

    def set_styles(
        self, styles: Optional[Union[EdgeStyle, List[EdgeStyle]]] = None, **attrs
    ) -> "Edge":
        """Explicit method to update style."""
        # This method is renamed from style() to set_styles() to avoid conflict with 'style' attribute field.
        return self(styles=styles, **attrs)

    def __rshift__(self, other: Union["Node", tuple]) -> "EdgeChain":
        """Support edge >> node syntax (chaining) and tuple fan-out."""
        if isinstance(other, tuple):
            return EdgeChain([self] + [Edge(self.target, node) for node in other])
        return EdgeChain([self, Edge(self.target, other)])

    @property
    def attrs(self) -> Dict[str, Any]:
        """Return all attributes as a dictionary (for renderer compatibility)."""
        # Return merged dict of model fields and extras
        # Exclude 'source' and 'target' from attributes dict as they are structural and handled separately by renderer
        return self.model_dump(
            exclude_none=True, by_alias=True, exclude={"source", "target"}
        )

    @property
    def _attrs(self) -> Dict[str, Any]:
        """Backward compatibility for renderer accessing ._attrs"""
        return self.attrs


class EdgeChain:
    """Represents a chain of edges (e.g. a >> b >> c)."""

    def __init__(self, edges: List[Edge]):
        self.edges = edges

    def __rshift__(self, other: Union["Node", tuple]) -> "EdgeChain":
        """Support chain >> node syntax and tuple fan-out."""
        last_edge = self.edges[-1]
        if isinstance(other, tuple):
            # Fan-out: create edges from last target to all nodes in tuple
            for node in other:
                self.edges.append(Edge(last_edge.target, node))
        else:
            new_edge = Edge(last_edge.target, other)
            self.edges.append(new_edge)
        return self

    def __or__(
        self, styles: Union[EdgeStyle, List[EdgeStyle], Dict[str, Any]]
    ) -> "EdgeChain":
        """Apply style to all edges in chain: chain | style"""
        # Check if it's a DiagramEdge or similar object with to_style() method
        if hasattr(styles, "to_style"):
            styles = styles.to_style()

        for edge in self.edges:
            edge | styles
        return self

    def set_styles(
        self, styles: Optional[Union[EdgeStyle, List[EdgeStyle]]] = None, **attrs
    ) -> "EdgeChain":
        """Explicit method to update style for all edges in chain."""
        for edge in self.edges:
            # Call __call__ to update style/attributes since .style() method is shadowed/problematic
            # We can use the __call__ method we defined in Edge
            edge(styles=styles, **attrs)
        return self


# Alias for backward compatibility or if Node still expects it
EdgeBuilder = EdgeChain
