from dataclasses import dataclass
from typing import Dict

from .constants import (
    BLACK,
    BOX,
    CIRCLE,
    DASHED,
    ELLIPSE,
    FILLED,
    GRAY,
    LIGHTBLUE,
    LIGHTGRAY,
    ROUNDED,
    SOLID,
    WHITE,
)
from .style import EdgeStyle, GraphStyle, NodeStyle


@dataclass
class Theme:
    name: str
    graph: GraphStyle
    node: NodeStyle
    edge: EdgeStyle


# 1. Default Theme
DEFAULT_THEME = Theme(
    name="default",
    graph=GraphStyle(bgcolor=WHITE, fontname="Helvetica"),
    node=NodeStyle(
        shape=BOX,
        style=f"{FILLED},{ROUNDED}",
        fillcolor=LIGHTBLUE,
        fontname="Helvetica",
        penwidth=1,
    ),
    edge=EdgeStyle(color=GRAY, fontname="Helvetica"),
)

# 2. Dark Theme
DARK_THEME = Theme(
    name="dark",
    graph=GraphStyle(bgcolor="#2d2d2d", fontname="Helvetica", fontcolor=WHITE),
    node=NodeStyle(
        shape=BOX,
        style=f"{FILLED},{ROUNDED}",
        fillcolor="#4d4d4d",
        fontcolor=WHITE,
        color=LIGHTGRAY,
        fontname="Helvetica",
    ),
    edge=EdgeStyle(color=LIGHTGRAY, fontcolor=LIGHTGRAY, fontname="Helvetica"),
)

# 3. Pastel Theme
PASTEL_THEME = Theme(
    name="pastel",
    graph=GraphStyle(bgcolor="#fdfbf7", fontname="Comic Sans MS"),
    node=NodeStyle(
        shape=ELLIPSE,
        style=FILLED,
        fillcolor="#ffb7b2",  # Pastel red/pink
        color="#ffb7b2",
        fontname="Comic Sans MS",
    ),
    edge=EdgeStyle(
        color="#aac7d8", penwidth=2, fontname="Comic Sans MS"
    ),  # Pastel blue
)

# 4. Blueprint Theme
BLUEPRINT_THEME = Theme(
    name="blueprint",
    graph=GraphStyle(bgcolor="#1a237e", fontcolor=WHITE, fontname="Courier"),
    node=NodeStyle(
        shape=BOX,
        style=FILLED,
        fillcolor="#1a237e",  # Same as bg
        color=WHITE,  # White border
        fontcolor=WHITE,
        penwidth=2,
        fontname="Courier",
    ),
    edge=EdgeStyle(color=WHITE, style=DASHED, fontcolor=WHITE, fontname="Courier"),
)

# 5. Forest Theme
FOREST_THEME = Theme(
    name="forest",
    graph=GraphStyle(bgcolor="#e8f5e9", fontname="Times-Roman"),
    node=NodeStyle(
        shape=CIRCLE,
        style=FILLED,
        fillcolor="#a5d6a7",  # Light green
        color="#2e7d32",  # Dark green border
        fontcolor="#1b5e20",
        fontname="Times-Roman",
    ),
    edge=EdgeStyle(color="#5d4037", penwidth=1.5, fontname="Times-Roman"),  # Brown
)

# 6. Ocean Theme
OCEAN_THEME = Theme(
    name="ocean",
    graph=GraphStyle(bgcolor="#e0f7fa", fontname="Helvetica"),
    node=NodeStyle(
        shape=BOX,
        style=f"{FILLED},{ROUNDED}",
        fillcolor="#4dd0e1",  # Cyan
        color="#006064",  # Dark cyan
        fontcolor="#006064",
        fontname="Helvetica",
    ),
    edge=EdgeStyle(color="#0277bd", fontcolor="#0277bd", fontname="Helvetica"),  # Blue
)

# 7. Minimal Theme
MINIMAL_THEME = Theme(
    name="minimal",
    graph=GraphStyle(bgcolor=WHITE, fontname="Helvetica"),
    node=NodeStyle(
        shape=BOX,
        style=SOLID,  # Not filled
        color=BLACK,
        fontcolor=BLACK,
        penwidth=1,
        fontname="Helvetica",
    ),
    edge=EdgeStyle(color=BLACK, fontcolor=BLACK, fontname="Helvetica"),
)

# Registry
THEMES: Dict[str, Theme] = {
    "default": DEFAULT_THEME,
    "dark": DARK_THEME,
    "pastel": PASTEL_THEME,
    "blueprint": BLUEPRINT_THEME,
    "forest": FOREST_THEME,
    "ocean": OCEAN_THEME,
    "minimal": MINIMAL_THEME,
}
