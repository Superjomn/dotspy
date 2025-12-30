from .constants import *
from .style import EdgeStyle, GraphStyle, NodeStyle

# Node styles
BOX_NODE = NodeStyle(shape=BOX, style=FILLED, fillcolor=LIGHTBLUE)
ROUNDED_BOX = NodeStyle(shape=BOX, style=f"{FILLED},{ROUNDED}", fillcolor=LIGHTGRAY)
CIRCLE_NODE = NodeStyle(shape=CIRCLE, style=FILLED, fillcolor=LIGHTBLUE)
DIAMOND_NODE = NodeStyle(shape=DIAMOND, style=FILLED, fillcolor=YELLOW)
RECORD_NODE = NodeStyle(shape=RECORD, style=FILLED, fillcolor=WHITE)
INVISIBLE_NODE = NodeStyle(style=INVISIBLE)

# Decision/condition node
DECISION_NODE = NodeStyle(shape=DIAMOND, style=FILLED, fillcolor=YELLOW)
# Process node
PROCESS_NODE = NodeStyle(shape=BOX, style=FILLED, fillcolor=LIGHTBLUE)
# Terminal node (start/end)
TERMINAL_NODE = NodeStyle(shape=ELLIPSE, style=FILLED, fillcolor=LIGHTGRAY)
# Input/output node
IO_NODE = NodeStyle(
    shape="parallelogram", style=FILLED, fillcolor="lightyellow"
)  # Use string literal if constant missing

# Edge styles
DASHED_EDGE = EdgeStyle(style=DASHED)
DOTTED_EDGE = EdgeStyle(style=DOTTED)
BOLD_EDGE = EdgeStyle(style=BOLD, penwidth=2)
RED_EDGE = EdgeStyle(color=RED)
BLUE_EDGE = EdgeStyle(color=BLUE)
GREEN_EDGE = EdgeStyle(color=GREEN)
NO_ARROW = EdgeStyle(arrowhead=NONE)
BIDIRECTIONAL = EdgeStyle(dir="both")

# Graph styles
LR_GRAPH = GraphStyle(rankdir=LR)
TB_GRAPH = GraphStyle(rankdir=TB)
COMPACT_GRAPH = GraphStyle(nodesep=0.3, ranksep=0.3)
SPACED_GRAPH = GraphStyle(nodesep=1.0, ranksep=1.0)
