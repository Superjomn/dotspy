from typing import Any, Dict, Optional, TYPE_CHECKING
from .context import get_current_graph, get_current_subgraph, get_active_node_styles
from .style import NodeStyle

if TYPE_CHECKING:
    from .edge import EdgeBuilder

class Node:
    _id_counter = 0
    
    def __init__(
        self,
        name: Optional[str] = None,
        style: Optional[NodeStyle] = None,
        nstyle: Optional[NodeStyle] = None,
        **attrs
    ):
        # Generate unique ID if name not provided
        self._name = name or self._generate_name()
        
        # Support both style and nstyle for NodeStyle objects
        # nstyle is preferred for explicit NodeStyle objects to avoid confusion with DOT style string
        actual_style = nstyle if nstyle else style

        # Merge active context styles with provided style and attrs
        self._attrs = self._resolve_attrs(actual_style, attrs)
        
        # Register with current graph/subgraph
        self._register()
    
    @classmethod
    def _generate_name(cls) -> str:
        cls._id_counter += 1
        return f"node_{cls._id_counter}"
    
    def _resolve_attrs(self, style, attrs) -> Dict[str, Any]:
        """Merge context styles, provided style, and direct attrs."""
        result = {}
        # Apply context styles first (in order)
        for ctx_style in get_active_node_styles():
            result.update(ctx_style.to_dict())
        # Apply provided style
        if style:
            if isinstance(style, NodeStyle):
                result.update(style.to_dict())
            else:
                result["style"] = style  # Direct DOT style string
        # Apply direct attrs (highest priority)
        result.update(attrs)
        return result
    
    def _register(self):
        """Register this node with current subgraph or graph."""
        subgraph = get_current_subgraph()
        if subgraph:
            subgraph._add_node(self)
        else:
            graph = get_current_graph()
            if graph:
                graph._add_node(self)
    
    def __rshift__(self, other: "Node") -> "EdgeBuilder":
        """Support node1 >> node2 syntax."""
        from .edge import Edge, EdgeChain
        # We wrap even a single edge in EdgeChain to support consistent chaining behavior
        # e.g. (a >> b) >> c
        return EdgeChain([Edge(self, other)])
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def attrs(self) -> Dict[str, Any]:
        return self._attrs.copy()
