import uuid
import tempfile
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from pydantic import Field, PrivateAttr, ConfigDict
from .context import (
    set_current_graph, reset_current_graph,
    set_current_subgraph, reset_current_subgraph,
    set_graph as set_singleton_graph,
    get_current_graph,
    get_current_subgraph
)
from .style import GraphStyle, merge_styles
from .constants import DIGRAPH, TB
from .attributes import GraphAttributes

if TYPE_CHECKING:
    from .node import Node
    from .edge import Edge

class Graph(GraphAttributes):
    """Main graph container."""
    
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    name: str = Field("G", description="Graph name.")
    graph_type: str = Field(DIGRAPH, description="Graph type (digraph or graph).")
    
    # Internal state
    _nodes: List["Node"] = PrivateAttr(default_factory=list)
    _edges: List["Edge"] = PrivateAttr(default_factory=list)
    _subgraphs: List["Subgraph"] = PrivateAttr(default_factory=list)
    _token: Any = PrivateAttr(default=None)
    
    def __init__(
        self,
        name: str = "G",
        graph_type: str = DIGRAPH,
        styles: Optional[Union[GraphStyle, List[GraphStyle]]] = None,
        rankdir: Optional[str] = None,
        **attrs
    ):
        style_attrs = merge_styles(styles)
            
        # rankdir default handling
        combined_attrs = {**style_attrs, **attrs}
        if rankdir:
            combined_attrs['rankdir'] = rankdir
        elif 'rankdir' not in combined_attrs:
            combined_attrs['rankdir'] = TB
            
        super().__init__(name=name, graph_type=graph_type, **combined_attrs)
        
        # Explicit initialization of private attributes to fix Pydantic issues
        # Use simple assignment if Pydantic internals are failing
        object.__setattr__(self, '_nodes', [])
        object.__setattr__(self, '_edges', [])
        object.__setattr__(self, '_subgraphs', [])
        object.__setattr__(self, '_token', None)
    
    def __enter__(self) -> "Graph":
        token = set_current_graph(self)
        object.__setattr__(self, '_token', token)
        return self
    
    def __exit__(self, *args):
        if self._token:
            reset_current_graph(self._token)
    
    def _add_node(self, node: "Node"):
        self._nodes.append(node)
    
    def _add_edge(self, edge: "Edge"):
        self._edges.append(edge)
    
    def _add_subgraph(self, subgraph: "Subgraph"):
        self._subgraphs.append(subgraph)
    
    def to_dot(self) -> str:
        """Render to DOT format."""
        from .renderer import render_graph
        return render_graph(self)
    
    def render(self, filename: Optional[str] = None, format: str = "png"):
        """Render to file using graphviz."""
        from .utils import render_to_file
        if filename is None:
            filename = tempfile.mktemp(suffix=f".{format}")
        render_to_file(self.to_dot(), filename, format=format)
        
    def set_as_default(self):
        """Set this graph as the singleton default graph."""
        set_singleton_graph(self)

    def _repr_svg_(self):
        """Jupyter Notebook SVG representation."""
        from .utils import render_to_svg
        return render_to_svg(self.to_dot())

    def _repr_png_(self):
        """Jupyter Notebook PNG representation."""
        from .utils import render_to_data
        return render_to_data(self.to_dot(), format="png")
        
    @property
    def attrs(self) -> Dict[str, Any]:
        """Return all attributes as a dictionary (for renderer compatibility)."""
        data = self.model_dump(exclude_none=True, by_alias=True, exclude={'name', 'graph_type'})
        return data

    @property
    def _attrs(self) -> Dict[str, Any]:
        """Backward compatibility for renderer accessing ._attrs"""
        return self.attrs

class Subgraph(GraphAttributes):
    """Subgraph container."""
    
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    name: str = Field(..., description="Subgraph name.")
    cluster: bool = Field(True, description="Whether this is a cluster subgraph.")
    
    # Internal state
    _nodes: Dict[str, "Node"] = PrivateAttr(default_factory=dict)
    _edges: List["Edge"] = PrivateAttr(default_factory=list)
    _subgraphs: List["Subgraph"] = PrivateAttr(default_factory=list)
    _token: Any = PrivateAttr(default=None)
    
    def __init__(
        self,
        name: Optional[str] = None,
        cluster: bool = True,
        styles: Optional[Union[GraphStyle, List[GraphStyle]]] = None,
        **attrs
    ):
        # Normalize name
        if name is None:
            name = f"subgraph_{uuid.uuid4().hex}"
        
        if cluster and not name.startswith("cluster_"):
            name = f"cluster_{name}"
            
        style_attrs = merge_styles(styles)
            
        combined_attrs = {**style_attrs, **attrs}
        
        super().__init__(name=name, cluster=cluster, **combined_attrs)
        
        # Explicit initialization using object.__setattr__ to bypass Pydantic interception if necessary
        object.__setattr__(self, '_nodes', {})
        object.__setattr__(self, '_edges', [])
        object.__setattr__(self, '_subgraphs', [])
        object.__setattr__(self, '_token', None)
        
        # Register with parent graph
        self._register()

    def _register(self):
        subgraph = get_current_subgraph()
        if subgraph:
            subgraph._add_subgraph(self)
        else:
            graph = get_current_graph()
            if graph:
                graph._add_subgraph(self)
    
    def __enter__(self) -> "Subgraph":
        token = set_current_subgraph(self)
        object.__setattr__(self, '_token', token)
        return self
    
    def __exit__(self, *args):
        if self._token:
            reset_current_subgraph(self._token)
    
    def _add_node(self, node: "Node"):
        self._nodes[node.name] = node
        
    def _add_subgraph(self, subgraph: "Subgraph"):
        self._subgraphs.append(subgraph)
    
    def __getattr__(self, name: str) -> "Node":
        """Access nodes by name: subgraph.node_name"""
        # Pydantic 2 uses __getattr__ for extra fields if configured.
        # However, accessing private attributes shouldn't trigger this unless they are missing from __dict__
        # or __pydantic_private__.
        
        # If we are looking for a private attribute, we should probably fail fast or delegate to super
        # because our custom logic is only for Node lookup.
        if name.startswith("_"):
             raise AttributeError(name)

        # Attempt to access _nodes from private storage safely
        # Note: self._nodes is a PrivateAttr.
        # If it's not initialized, accessing it might be tricky during init.
        # But after init it should be fine.
        
        # The errors "AttributeError: 'Subgraph' object has no attribute '_nodes'" suggest
        # that _nodes is not being found. 
        # This usually happens if __init__ is overridden but super().__init__ isn't called correctly
        # or if Pydantic's init sequence is messed up.
        
        # We are calling super().__init__(...) in Subgraph.__init__.
        # But _nodes has a default factory.
        
        try:
            # Direct access to private attribute
            nodes = self._nodes
            if name in nodes:
                return nodes[name]
        except AttributeError:
            pass
            
        # Fallback to Pydantic attributes/methods
        try:
            return super().__getattr__(name)
        except AttributeError:
             raise AttributeError(f"No node named '{name}' in subgraph")

    @property
    def attrs(self) -> Dict[str, Any]:
        """Return all attributes as a dictionary (for renderer compatibility)."""
        data = self.model_dump(exclude_none=True, by_alias=True, exclude={'name', 'cluster'})
        return data

    @property
    def _attrs(self) -> Dict[str, Any]:
        """Backward compatibility for renderer accessing ._attrs"""
        return self.attrs

    @property
    def _name(self) -> str:
        """Compat property."""
        return self.name
