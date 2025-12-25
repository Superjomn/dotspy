from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph, Subgraph
    from .node import Node
    from .edge import Edge

def escape_string(s: str) -> str:
    """Escape special characters in DOT strings."""
    s = str(s)
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    return s

def format_attrs(attrs: Dict[str, Any]) -> str:
    """Format attributes as DOT attribute string."""
    if not attrs:
        return ""
    parts = []
    for key, value in attrs.items():
        if isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, str):
            # Check if value is an HTML string (starts with < and ends with >) - simplistic check
            # DOT allows HTML-like labels.
            if value.startswith("<") and value.endswith(">"):
                pass # Don't quote HTML labels
            else:
                value = f'"{escape_string(value)}"'
        else:
             value = f'"{escape_string(str(value))}"'
        parts.append(f"{key}={value}")
    return f"[{', '.join(parts)}]"

def render_node(node: "Node", indent: str = "  ") -> str:
    """Render a node to DOT format."""
    attrs_str = format_attrs(node.attrs)
    if attrs_str:
        return f'{indent}"{node.name}" {attrs_str};'
    return f'{indent}"{node.name}";'

def render_edge(edge: "Edge", is_digraph: bool, indent: str = "  ") -> str:
    """Render an edge to DOT format."""
    arrow = "->" if is_digraph else "--"
    attrs_str = format_attrs(edge._attrs)
    if attrs_str:
        return f'{indent}"{edge.source.name}" {arrow} "{edge.target.name}" {attrs_str};'
    return f'{indent}"{edge.source.name}" {arrow} "{edge.target.name}";'

def render_subgraph(subgraph: "Subgraph", is_digraph: bool, indent: str = "  ") -> str:
    """Render a subgraph to DOT format."""
    lines = []
    lines.append(f'{indent}subgraph "{subgraph._name}" {{')
    
    # Subgraph attributes
    inner_indent = indent + "  "
    for key, value in subgraph._attrs.items():
        if isinstance(value, str):
             if not (value.startswith("<") and value.endswith(">")):
                value = f'"{escape_string(value)}"'
        else:
             value = f'"{escape_string(str(value))}"'
        lines.append(f"{inner_indent}{key}={value};")
    
    # Nodes
    for node in subgraph._nodes.values():
        lines.append(render_node(node, inner_indent))
    
    # Edges (if subgraph tracks them - currently Subgraph doesn't have add_edge, but Graph does)
    # Graph.py Subgraph class has _edges list.
    for edge in subgraph._edges:
        lines.append(render_edge(edge, is_digraph, inner_indent))
    
    lines.append(f"{indent}}}")
    return "\n".join(lines)

def render_graph(graph: "Graph") -> str:
    """Render a complete graph to DOT format."""
    is_digraph = graph.graph_type == "digraph"
    lines = []
    
    # Graph header
    lines.append(f'{graph.graph_type} "{graph.name}" {{')
    
    # Graph attributes
    for key, value in graph._attrs.items():
        if isinstance(value, str):
             if not (value.startswith("<") and value.endswith(">")):
                value = f'"{escape_string(value)}"'
        else:
             value = f'"{escape_string(str(value))}"'
        lines.append(f"  {key}={value};")
    
    # Subgraphs
    for subgraph in graph._subgraphs:
        lines.append(render_subgraph(subgraph, is_digraph))
    
    # Top-level nodes
    for node in graph._nodes:
        lines.append(render_node(node))
    
    # Top-level edges
    for edge in graph._edges:
        lines.append(render_edge(edge, is_digraph))
    
    lines.append("}")
    return "\n".join(lines)
