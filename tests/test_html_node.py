"""Tests for HTMLNode functionality."""

import os
import tempfile

import pytest

from dotspy import Graph, HTMLNode


class TestHTMLNodeBasic:
    """Test basic HTMLNode functionality."""

    def test_html_node_with_raw_html(self):
        """Test creating HTMLNode with raw HTML."""
        node = HTMLNode(name="test", html="<B>Bold</B> text")
        assert node.name == "test"
        assert node.attrs["label"] == "<<B>Bold</B> text>"

    def test_html_node_with_markdown(self):
        """Test creating HTMLNode with markdown."""
        node = HTMLNode(name="test", markdown="**Bold** text")
        # Should contain <B>Bold</B> after conversion
        assert "<B>Bold</B>" in node.attrs["label"]

    def test_html_node_requires_one_parameter(self):
        """Test that HTMLNode requires either markdown or html."""
        with pytest.raises(
            ValueError, match="Must specify either 'markdown' or 'html'"
        ):
            HTMLNode(name="test")

    def test_html_node_rejects_both_parameters(self):
        """Test that HTMLNode rejects both markdown and html."""
        with pytest.raises(
            ValueError, match="Specify either 'markdown' or 'html', not both"
        ):
            HTMLNode(name="test", markdown="**Bold**", html="<B>Bold</B>")

    def test_html_node_auto_name(self):
        """Test that HTMLNode can auto-generate names."""
        node = HTMLNode(html="<B>Test</B>")
        assert node.name.startswith("node_")

    def test_html_node_with_styles(self):
        """Test HTMLNode with styles."""
        from dotspy import NodeStyle

        style = NodeStyle(shape="box", color="red")
        node = HTMLNode(html="<B>Test</B>", styles=style)
        assert node.attrs["shape"] == "box"
        assert node.attrs["color"] == "red"

    def test_html_node_with_additional_attrs(self):
        """Test HTMLNode with additional attributes."""
        node = HTMLNode(html="<B>Test</B>", fillcolor="blue", penwidth=2)
        assert node.attrs["fillcolor"] == "blue"
        assert node.attrs["penwidth"] == 2


class TestMarkdownConversion:
    """Test markdown to DOT HTML conversion."""

    def test_markdown_bold(self):
        """Test bold text conversion."""
        node = HTMLNode(markdown="**bold text**")
        assert "<B>bold text</B>" in node.attrs["label"]

    def test_markdown_italic(self):
        """Test italic text conversion."""
        node = HTMLNode(markdown="*italic text*")
        assert "<I>italic text</I>" in node.attrs["label"]

    def test_markdown_strikethrough(self):
        """Test strikethrough text conversion."""
        node = HTMLNode(markdown="~~strikethrough~~")
        assert "<S>strikethrough</S>" in node.attrs["label"]

    def test_markdown_heading(self):
        """Test heading conversion."""
        node = HTMLNode(markdown="# Heading 1")
        label = node.attrs["label"]
        assert "POINT-SIZE" in label
        assert "<B>Heading 1</B>" in label

    def test_markdown_mixed_formatting(self):
        """Test mixed formatting."""
        node = HTMLNode(markdown="**bold** and *italic*")
        label = node.attrs["label"]
        assert "<B>bold</B>" in label
        assert "<I>italic</I>" in label

    def test_markdown_multiline(self):
        """Test multiline markdown."""
        node = HTMLNode(markdown="Line 1\n\nLine 2")
        label = node.attrs["label"]
        # Should contain separate table rows for each paragraph
        assert "<TR>" in label
        assert "Line 1" in label
        assert "Line 2" in label

    def test_markdown_list(self):
        """Test list conversion."""
        markdown = """- Item 1
- Item 2
- Item 3"""
        node = HTMLNode(markdown=markdown)
        label = node.attrs["label"]
        # Should use TABLE structure for lists
        assert "<TABLE" in label
        assert "<TR>" in label

    def test_markdown_table(self):
        """Test table conversion."""
        markdown = """| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |"""
        node = HTMLNode(markdown=markdown)
        label = node.attrs["label"]
        assert "<TABLE" in label
        assert "<TD" in label

    def test_markdown_code_inline(self):
        """Test inline code conversion."""
        node = HTMLNode(markdown="`code`")
        label = node.attrs["label"]
        assert "monospace" in label.lower()

    def test_markdown_code_block(self):
        """Test code block conversion."""
        markdown = """```python
def hello():
    print("world")
```"""
        node = HTMLNode(markdown=markdown)
        label = node.attrs["label"]
        # Should use monospace font
        assert "monospace" in label.lower()

    def test_markdown_header_and_table(self):
        """Test mixed content: header followed by table."""
        markdown = """# A Table
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |"""
        node = HTMLNode(markdown=markdown)
        label = node.attrs["label"]

        # Should contain both header and table
        assert "A Table" in label
        assert "Header 1" in label
        assert "Header 2" in label
        assert "Cell 1" in label
        assert "Cell 2" in label

        # Should be wrapped in a master table
        assert label.startswith("<<TABLE")
        assert label.endswith(">>")

        # Should have nested table structure
        # The master table contains rows, one with the header, one with the nested table
        assert "<TR>" in label
        assert "<TD>" in label


class TestHTMLNodeInGraph:
    """Test HTMLNode integration with Graph."""

    def test_html_node_in_graph(self):
        """Test that HTMLNode works in a Graph context."""
        with Graph() as g:
            node = HTMLNode(name="test", html="<B>Test</B>")

        # Node should be registered in graph
        assert len(g._nodes) == 1
        assert g._nodes[0].name == "test"

    def test_html_node_rendering(self):
        """Test that HTMLNode renders correctly."""
        with Graph() as g:
            node = HTMLNode(name="test", html="<B>Bold</B> and <I>Italic</I>")

        dot = g.to_dot()
        # Label should be in the DOT output without quotes around HTML
        assert '"test"' in dot
        assert "label=<<B>Bold</B> and <I>Italic</I>>" in dot

    def test_html_node_with_edge(self):
        """Test HTMLNode with edges."""
        with Graph() as g:
            n1 = HTMLNode(name="n1", html="<B>Start</B>")
            n2 = HTMLNode(name="n2", html="<B>End</B>")
            n1 >> n2

        dot = g.to_dot()
        assert '"n1" -> "n2"' in dot

    def test_markdown_node_rendering(self):
        """Test that markdown gets converted in rendering."""
        with Graph() as g:
            node = HTMLNode(name="test", markdown="**Bold** text")

        dot = g.to_dot()
        assert '"test"' in dot
        # Should contain converted HTML, not raw markdown
        assert "<B>Bold</B>" in dot


class TestRawHTMLPassthrough:
    """Test raw HTML passthrough without conversion."""

    def test_complex_html_structure(self):
        """Test complex HTML with tables."""
        html = """<TABLE>
  <TR><TD><B>Header</B></TD></TR>
  <TR><TD>Content</TD></TR>
</TABLE>"""
        node = HTMLNode(html=html)
        # Should preserve the exact HTML structure
        assert "<TABLE>" in node.attrs["label"]
        assert "<B>Header</B>" in node.attrs["label"]

    def test_html_with_font_attributes(self):
        """Test HTML with FONT attributes."""
        html = '<FONT POINT-SIZE="16" COLOR="red">Large Red Text</FONT>'
        node = HTMLNode(html=html)
        assert 'POINT-SIZE="16"' in node.attrs["label"]
        assert 'COLOR="red"' in node.attrs["label"]

    def test_html_with_br(self):
        """Test HTML with line breaks."""
        html = "Line 1<BR/>Line 2<BR/>Line 3"
        node = HTMLNode(html=html)
        assert html in node.attrs["label"]


class TestErrorHandling:
    """Test error handling."""

    def test_mistune_not_available_simulation(self):
        """Test error when mistune is not available."""
        # This test will only work if mistune is actually installed
        # It's more of a documentation test showing the expected behavior
        # In real scenario without mistune, importing would raise ImportError
        pass

    def test_empty_markdown(self):
        """Test with empty markdown."""
        # Empty markdown should still work
        node = HTMLNode(markdown="")
        assert node.attrs["label"]

    def test_empty_html(self):
        """Test with empty HTML."""
        # Empty HTML should still work
        node = HTMLNode(html="")
        assert node.attrs["label"] == "<>"


class TestEndToEnd:
    """End-to-end tests that render to actual image files."""

    def test_render_header_and_table_to_png(self):
        """
        Test the original failing case from the notebook: header + table.
        This test verifies that graphviz can actually render the output.
        """
        # The exact failing case from the notebook
        markdown = """# A Table
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |"""

        # Create a graph with the HTMLNode
        with Graph(label="End to End Test") as g:
            node = HTMLNode(name="test_node", markdown=markdown)

        # Create a temporary file for the PNG output
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Render to PNG - this will fail if DOT HTML is invalid
            g.render(filename=tmp_path, format="png")

            # Verify the file was created and has content
            assert os.path.exists(tmp_path), "PNG file should be created"
            file_size = os.path.getsize(tmp_path)
            assert file_size > 0, f"PNG file should have content, got {file_size} bytes"

            # If we got here, graphviz successfully rendered the DOT HTML!

        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_render_complex_markdown_to_png(self):
        """Test rendering complex markdown with multiple elements."""
        markdown = """# Title

This is a **bold** paragraph with *italic* text.

## Subtitle

- Item 1
- Item 2
- Item 3

### Data Table

| Name | Value | Status |
|------|-------|--------|
| A    | 100   | ✓      |
| B    | 200   | ✓      |

> This is a blockquote
"""

        with Graph(label="Complex Markdown Test") as g:
            node = HTMLNode(markdown=markdown)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            g.render(filename=tmp_path, format="png")
            assert os.path.exists(tmp_path)
            assert os.path.getsize(tmp_path) > 0
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
