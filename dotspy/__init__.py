"""dotspy - A Pythonic wrapper for Graphviz DOT language."""

from .constants import *
from .node import Node
from .edge import Edge
from .graph import Graph, Subgraph
from .style import NodeStyle, EdgeStyle, GraphStyle
from .builtin_styles import (
    BOX_NODE, ROUNDED_BOX, CIRCLE_NODE, DIAMOND_NODE, RECORD_NODE,
    DECISION_NODE, PROCESS_NODE, TERMINAL_NODE, INVISIBLE_NODE,
    DASHED_EDGE, DOTTED_EDGE, BOLD_EDGE, RED_EDGE, BLUE_EDGE, GREEN_EDGE,
    NO_ARROW, BIDIRECTIONAL,
    LR_GRAPH, TB_GRAPH, COMPACT_GRAPH, SPACED_GRAPH,
)
from .context import set_graph, get_graph
from .utils import render_to_file, render_to_svg

__version__ = "0.1.0"
__all__ = [
    # Core classes
    "Node", "Edge", "Graph", "Subgraph",
    # Style classes
    "NodeStyle", "EdgeStyle", "GraphStyle",
    # Singleton functions
    "set_graph", "get_graph",
    # Utility functions
    "render_to_file", "render_to_svg",
    # Constants
    "RECT", "BOX", "CIRCLE", "ELLIPSE", "DIAMOND", "PLAINTEXT", "POINT", "RECORD", "POLYGON",
    "TRIANGLE", "SQUARE", "STAR",
    "FILLED", "SOLID", "DASHED", "DOTTED", "BOLD", "ROUNDED", "INVISIBLE",
    "RED", "BLUE", "GREEN", "BLACK", "WHITE", "GRAY", "YELLOW", "ORANGE", "PURPLE", "CYAN", "MAGENTA",
    "LIGHTBLUE", "LIGHTGRAY", "DARKGRAY",
    "DIGRAPH", "GRAPH",
    "TB", "BT", "LR", "RL",
    "NORMAL", "NONE", "VEE", "DIAMOND_ARROW", "DOT_ARROW", "OPEN", "BOX_ARROW",
    "HELVETICA", "TIMES", "COURIER",
    # Builtin styles
    "BOX_NODE", "ROUNDED_BOX", "CIRCLE_NODE", "DIAMOND_NODE", "RECORD_NODE",
    "DECISION_NODE", "PROCESS_NODE", "TERMINAL_NODE", "INVISIBLE_NODE",
    "DASHED_EDGE", "DOTTED_EDGE", "BOLD_EDGE", "RED_EDGE", "BLUE_EDGE", "GREEN_EDGE",
    "NO_ARROW", "BIDIRECTIONAL",
    "LR_GRAPH", "TB_GRAPH", "COMPACT_GRAPH", "SPACED_GRAPH",
]
