import uuid
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from .context import (
    set_current_graph, reset_current_graph,
    set_current_subgraph, reset_current_subgraph,
    set_graph as set_singleton_graph,
    get_current_graph
)
from .style import GraphStyle
from .constants import DIGRAPH, TB

if TYPE_CHECKING:
    from .node import Node
    from .edge import Edge

class Graph:
    """Main graph container."""
    
    def __init__(
        self,
        name: str = "G",
        graph_type: str = DIGRAPH,
        style: Optional[GraphStyle] = None,
        rankdir: Optional[str] = None,
        **attrs
    ):
        self.name = name
        self.graph_type = graph_type
        self._attrs = {}
        
        if style:
            self._attrs.update(style.to_dict())
            
        if rankdir:
            self._attrs["rankdir"] = rankdir
        elif "rankdir" not in self._attrs:
            self._attrs["rankdir"] = TB
            
        self._attrs.update(attrs)
        
        self._nodes: List["Node"] = []
        self._edges: List["Edge"] = []
        self._subgraphs: List["Subgraph"] = []
        
        self._token = None
        
        # Set as singleton if not already set? Or just allow explicit setting.
        # Ideally, we don't auto-set singleton.
    
    def __enter__(self) -> "Graph":
        self._token = set_current_graph(self)
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
    
    def render(self, filename: str, format: str = "png"):
        """Render to file using graphviz."""
        from .utils import render_to_file
        render_to_file(self.to_dot(), filename, format=format)
        
    def set_as_default(self):
        """Set this graph as the singleton default graph."""
        set_singleton_graph(self)

class Subgraph:
    """Subgraph container."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        cluster: bool = True,
        style: Optional[GraphStyle] = None,
        **attrs
    ):
        # If cluster=True and name doesn't start with "cluster_", prefix it
        self._cluster = cluster
        self._name = self._normalize_name(name, cluster)
        
        self._attrs = {}
        if style:
            self._attrs.update(style.to_dict())
        self._attrs.update(attrs)
        
        self._nodes: Dict[str, "Node"] = {}  # name -> Node mapping
        self._edges: List["Edge"] = []
        
        self._token = None
        
        # Register with parent graph
        self._register()
    
    def _normalize_name(self, name: Optional[str], cluster: bool) -> str:
        if name is None:
            name = f"subgraph_{uuid.uuid4().hex}"
        
        if cluster and not name.startswith("cluster_"):
            return f"cluster_{name}"
        return name

    @property
    def name(self) -> str:
        return self._name

    def _register(self):
        graph = get_current_graph()
        if graph:
            graph._add_subgraph(self)
    
    def __enter__(self) -> "Subgraph":
        self._token = set_current_subgraph(self)
        return self
    
    def __exit__(self, *args):
        if self._token:
            reset_current_subgraph(self._token)
    
    def _add_node(self, node: "Node"):
        self._nodes[node.name] = node
    
    def __getattr__(self, name: str) -> "Node":
        """Access nodes by name: subgraph.node_name"""
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._nodes:
            return self._nodes[name]
        raise AttributeError(f"No node named '{name}' in subgraph")
