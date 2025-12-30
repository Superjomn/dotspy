from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class BaseAttributes(BaseModel):
    """Base attributes for all Graphviz elements."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    label: Optional[str] = Field(None, description="Text label attached to objects.")
    comment: Optional[str] = Field(None, description="Comments inserted into output.")

    # Common identification/URL attributes
    URL: Optional[str] = Field(
        None, description="Hyperlink associated with the object."
    )
    href: Optional[str] = Field(None, description="Synonym for URL.")
    target: Optional[str] = Field(None, description="Target frame for URL.")
    tooltip: Optional[str] = Field(None, description="Tooltip annotation.")


class ColorAttributes(BaseModel):
    """Color-related attributes."""

    color: Optional[str] = Field(None, description="Basic drawing color.")
    fillcolor: Optional[str] = Field(
        None, description="Color used to fill the background of node or cluster."
    )
    fontcolor: Optional[str] = Field(None, description="Color used for text.")
    bgcolor: Optional[Union[str, list]] = Field(
        None, description="Background color for drawing, plus initial fill color."
    )


class FontAttributes(BaseModel):
    """Font-related attributes."""

    fontname: Optional[str] = Field(None, description="Font used for text.")
    fontsize: Optional[Union[float, str]] = Field(
        None, description="Font size, in points."
    )


class SizeAttributes(BaseModel):
    """Size and dimension attributes."""

    width: Optional[Union[float, str]] = Field(None, description="Width in inches.")
    height: Optional[Union[float, str]] = Field(None, description="Height in inches.")
    penwidth: Optional[float] = Field(None, description="Width of the pen, in points.")
    margin: Optional[Union[float, str]] = Field(None, description="Margin.")


class NodeAttributes(BaseAttributes, ColorAttributes, FontAttributes, SizeAttributes):
    """Attributes specific to Nodes."""

    shape: Optional[str] = Field(
        None, description="Node shape (e.g., box, ellipse, circle, record)."
    )
    style: Optional[str] = Field(
        None, description="Graphics style (e.g., filled, rounded, dashed)."
    )
    sides: Optional[int] = Field(None, description="Number of sides if shape=polygon.")
    peripheries: Optional[int] = Field(
        None, description="Number of peripheries used for polygon and curve shapes."
    )
    fixedsize: Optional[Union[bool, str]] = Field(
        None, description="If true, node size is specified by width and height."
    )
    imagescale: Optional[Union[bool, str]] = Field(
        None, description="Whether to scale image."
    )
    image: Optional[str] = Field(None, description="Image file to display.")
    group: Optional[str] = Field(None, description="Group name for clustering.")
    pos: Optional[str] = Field(None, description="Position of node.")


class EdgeAttributes(BaseAttributes, ColorAttributes, FontAttributes, SizeAttributes):
    """Attributes specific to Edges."""

    style: Optional[str] = Field(
        None, description="Graphics style (e.g., solid, dashed)."
    )
    arrowhead: Optional[str] = Field(
        None, description="Style of arrowhead at the target end."
    )
    arrowtail: Optional[str] = Field(
        None, description="Style of arrowhead at the source end."
    )
    dir: Optional[str] = Field(
        None, description="Direction type for edges (forward, back, both, none)."
    )
    constraint: Optional[bool] = Field(
        None, description="If false, edge is not used in rank assignment."
    )
    weight: Optional[Union[float, int]] = Field(None, description="Weight of the edge.")
    minlen: Optional[int] = Field(
        None, description="Minimum rank distance between head and tail."
    )
    headlabel: Optional[str] = Field(
        None, description="Label placed near head of edge."
    )
    taillabel: Optional[str] = Field(
        None, description="Label placed near tail of edge."
    )
    lhead: Optional[str] = Field(None, description="Logical head of an edge.")
    ltail: Optional[str] = Field(None, description="Logical tail of an edge.")
    decorate: Optional[bool] = Field(
        None, description="If true, attach label to edge line."
    )


class GraphAttributes(BaseAttributes, ColorAttributes, FontAttributes, SizeAttributes):
    """Attributes specific to Graphs/Subgraphs."""

    rankdir: Optional[str] = Field(None, description="Rank direction (TB, LR, BT, RL).")
    layout: Optional[str] = Field(
        None, description="Layout engine to use (dot, neato, fdp, etc.)."
    )
    splines: Optional[Union[str, bool]] = Field(
        None,
        description="Control how edges are represented (spline, line, ortho, etc.).",
    )
    nodesep: Optional[Union[float, str]] = Field(
        None, description="Minimum space between two adjacent nodes in the same rank."
    )
    ranksep: Optional[Union[float, str]] = Field(
        None, description="Minimum separation between ranks."
    )
    compound: Optional[bool] = Field(None, description="Allow edges between clusters.")
    concentrate: Optional[bool] = Field(
        None, description="Merge multiple edges into one."
    )
    dpi: Optional[Union[float, int]] = Field(
        None, description="Dots per inch for image output."
    )
    newrank: Optional[bool] = Field(
        None, description="Use new rank assignment algorithm."
    )
    outputorder: Optional[str] = Field(
        None, description="Order in which nodes and edges are drawn."
    )
    rotate: Optional[int] = Field(
        None, description="If 90, set drawing orientation to landscape."
    )
    ratio: Optional[Union[str, float]] = Field(None, description="Aspect ratio.")
    center: Optional[bool] = Field(None, description="Center drawing on page.")
