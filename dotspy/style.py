from typing import Any, Dict, Optional
from .context import push_node_style, pop_node_style, push_edge_style, pop_edge_style

class BaseStyle:
    """Base class for all styles."""
    def __init__(self, **attrs):
        self._attrs = attrs
        self._token = None
    
    def __enter__(self):
        # Push style to context
        # This implementation needs to be overridden or handled by subclasses
        # because we need to know if it is a node style or edge style to push to correct stack
        pass
    
    def __exit__(self, *args):
        # Pop style from context
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        return self._attrs.copy()
    
    def merge(self, other: "BaseStyle") -> "BaseStyle":
        """Merge another style into this one (other takes precedence)."""
        new_attrs = self._attrs.copy()
        new_attrs.update(other._attrs)
        return self.__class__(**new_attrs)

class NodeStyle(BaseStyle):
    """Style for nodes."""
    # Supports: shape, style, color, fillcolor, fontcolor, fontname, fontsize,
    #           width, height, penwidth, label, etc.
    
    def __enter__(self):
        self._token = push_node_style(self)
        return self
    
    def __exit__(self, *args):
        if self._token:
            pop_node_style(self._token)

class EdgeStyle(BaseStyle):
    """Style for edges."""
    # Supports: color, style, penwidth, arrowhead, arrowtail, label,
    #           fontcolor, fontname, fontsize, dir, constraint, etc.
    
    def __enter__(self):
        self._token = push_edge_style(self)
        return self
    
    def __exit__(self, *args):
        if self._token:
            pop_edge_style(self._token)

class GraphStyle(BaseStyle):
    """Style for graphs/subgraphs."""
    # Supports: rankdir, bgcolor, fontname, fontsize, label, compound,
    #           splines, nodesep, ranksep, etc.
    pass
