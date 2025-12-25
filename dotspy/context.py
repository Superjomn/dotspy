from contextvars import ContextVar
from typing import Optional, List, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .graph import Graph, Subgraph
    from .style import NodeStyle, EdgeStyle

# Context variables
_current_graph: ContextVar[Optional["Graph"]] = ContextVar("current_graph", default=None)
_current_subgraph: ContextVar[Optional["Subgraph"]] = ContextVar("current_subgraph", default=None)
_active_node_styles: ContextVar[List["NodeStyle"]] = ContextVar("active_node_styles", default=[])
_active_edge_styles: ContextVar[List["EdgeStyle"]] = ContextVar("active_edge_styles", default=[])
_singleton_graph: Optional["Graph"] = None

def get_current_graph() -> Optional["Graph"]:
    return _current_graph.get()

def set_current_graph(graph: "Graph"):
    return _current_graph.set(graph)

def reset_current_graph(token):
    _current_graph.reset(token)

def get_current_subgraph() -> Optional["Subgraph"]:
    return _current_subgraph.get()

def set_current_subgraph(subgraph: "Subgraph"):
    return _current_subgraph.set(subgraph)

def reset_current_subgraph(token):
    _current_subgraph.reset(token)

def get_active_node_styles() -> List["NodeStyle"]:
    # Return a copy to prevent mutation of the list in context var if accessed directly
    # But for simplicity, we just return the list. Note that ContextVar stores immutable value by convention usually,
    # but here we store a list. Ideally we should copy on write.
    # For now, we'll return the list directly, but be careful not to mutate it in place in a way that affects other contexts incorrectly if shared.
    # Actually, ContextVars are thread-local/task-local.
    styles = _active_node_styles.get()
    return styles

def push_node_style(style: "NodeStyle"):
    current = _active_node_styles.get()
    # Create new list to avoid affecting parent context if we were just using the same list object
    new_styles = current + [style]
    return _active_node_styles.set(new_styles)

def pop_node_style(token):
    _active_node_styles.reset(token)

def get_active_edge_styles() -> List["EdgeStyle"]:
    return _active_edge_styles.get()

def push_edge_style(style: "EdgeStyle"):
    current = _active_edge_styles.get()
    new_styles = current + [style]
    return _active_edge_styles.set(new_styles)

def pop_edge_style(token):
    _active_edge_styles.reset(token)

def set_graph(graph: "Graph"):
    global _singleton_graph
    _singleton_graph = graph

def get_graph() -> Optional["Graph"]:
    return _singleton_graph
