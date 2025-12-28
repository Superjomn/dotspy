import pytest
from dotspy import Graph, Node

def test_repr_svg():
    g = Graph()
    g._add_node(Node("A"))
    svg = g._repr_svg_()
    assert isinstance(svg, str)
    assert svg.strip().startswith("<?xml") or svg.strip().startswith("<svg")
    assert "<svg" in svg

def test_repr_png():
    g = Graph()
    g._add_node(Node("A"))
    png_data = g._repr_png_()
    assert isinstance(png_data, bytes)
    # PNG magic number
    assert png_data.startswith(b'\x89PNG\r\n\x1a\n')


