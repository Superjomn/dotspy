from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from .context import get_current_graph, get_active_edge_styles
from .style import EdgeStyle

if TYPE_CHECKING:
    from .node import Node

class Edge:
    """Represents an edge between two nodes."""
    
    def __init__(
        self,
        source: "Node",
        target: "Node",
        style: Optional[EdgeStyle] = None,
        **attrs
    ):
        self.source = source
        self.target = target
        self._attrs = self._resolve_attrs(style, attrs)
        
        # Register with current graph
        self._register()
    
    def _resolve_attrs(self, style, attrs) -> Dict[str, Any]:
        """Merge context styles, provided style, and direct attrs."""
        result = {}
        for ctx_style in get_active_edge_styles():
            result.update(ctx_style.to_dict())
        if style:
            result.update(style.to_dict())
        result.update(attrs)
        return result
    
    def _register(self):
        graph = get_current_graph()
        if graph:
            graph._add_edge(self)
            
    def __call__(self, style: Optional[EdgeStyle] = None, **attrs) -> "Edge":
        """Update attributes: (node1 >> node2)(color="red")"""
        if style:
            self._attrs.update(style.to_dict())
        self._attrs.update(attrs)
        return self
    
    def __or__(self, style: Union[EdgeStyle, Dict[str, Any]]) -> "Edge":
        """Apply style: (node1 >> node2) | my_style"""
        if isinstance(style, dict):
            self._attrs.update(style)
        else:
            self(style=style)
        return self
    
    def __getitem__(self, style: EdgeStyle) -> "Edge":
        """Apply style: (node1 >> node2)[my_style]"""
        return self(style=style)

    def style(self, style: Optional[EdgeStyle] = None, **attrs) -> "Edge":
        """Explicit method to update style."""
        return self(style=style, **attrs)

    def __rshift__(self, other: "Node") -> "EdgeChain":
        """Support edge >> node syntax (chaining)."""
        return EdgeChain([self, Edge(self.target, other)])

class EdgeChain:
    """Represents a chain of edges (e.g. a >> b >> c)."""
    
    def __init__(self, edges: List[Edge]):
        self.edges = edges
        
    def __rshift__(self, other: "Node") -> "EdgeChain":
        """Support chain >> node syntax."""
        last_edge = self.edges[-1]
        new_edge = Edge(last_edge.target, other)
        self.edges.append(new_edge)
        return self
    
    def __or__(self, style: Union[EdgeStyle, Dict[str, Any]]) -> "EdgeChain":
        """Apply style to all edges in chain: chain | style"""
        for edge in self.edges:
            edge | style
        return self
    
    def style(self, style: Optional[EdgeStyle] = None, **attrs) -> "EdgeChain":
        """Explicit method to update style for all edges in chain."""
        for edge in self.edges:
            edge.style(style=style, **attrs)
        return self

# Alias for backward compatibility or if Node still expects it
EdgeBuilder = EdgeChain
