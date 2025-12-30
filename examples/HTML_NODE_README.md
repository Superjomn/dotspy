# HTMLNode - HTML-Like Labels for DOT Graphs

The `HTMLNode` class allows you to create nodes with rich HTML-like labels in your DOT graphs. It supports two modes:

## 1. Markdown Mode

Convert markdown syntax to DOT-compatible HTML automatically:

```python
import dotspy as ds

with ds.Graph() as g:
    # Simple formatting
    n1 = ds.HTMLNode(markdown="**Bold** and *italic*")
    
    # Headers with different sizes
    n2 = ds.HTMLNode(markdown="# Main Title")
    
    # Lists
    n3 = ds.HTMLNode(markdown="""
- Item 1
- Item 2
- Item 3
""")
    
    # Tables
    n4 = ds.HTMLNode(markdown="""
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
""")
```

### Supported Markdown Features

- **Bold**: `**text**` → `<B>text</B>`
- **Italic**: `*text*` → `<I>text</I>`
- **Strikethrough**: `~~text~~` → `<S>text</S>`
- **Headers**: `# H1` through `###### H6` with appropriate font sizes
- **Code**: `` `code` `` → monospace font
- **Lists**: Bullet lists using TABLE structure
- **Tables**: Full table support with headers and alignment
- **Blockquotes**: `> quote` → indented content
- **Mixed content**: Headers, paragraphs, tables, and other elements properly structured

### DOT HTML Structure

All markdown content is wrapped in a master table to ensure DOT compatibility:

```html
<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
  <TR><TD>First block (e.g., heading)</TD></TR>
  <TR><TD>Second block (e.g., paragraph)</TD></TR>
  <TR><TD><TABLE>...</TABLE></TD></TR>  <!-- Nested table for lists/tables -->
</TABLE>
```

This structure ensures that:
- All content is properly contained in a valid DOT HTML structure
- Mixed content (headers + tables, paragraphs + lists) renders correctly
- No invalid element siblings or orphaned tags

## 2. Raw HTML Mode

Provide DOT-compatible HTML directly for maximum control:

```python
import dotspy as ds

with ds.Graph() as g:
    # Simple HTML
    n1 = ds.HTMLNode(html="<B>Bold</B> and <I>Italic</I>")
    
    # Custom fonts
    n2 = ds.HTMLNode(html='<FONT POINT-SIZE="20" COLOR="red">Large Red Text</FONT>')
    
    # Complex tables
    n3 = ds.HTMLNode(html="""<TABLE BORDER="1">
  <TR><TD><B>Header</B></TD></TR>
  <TR><TD>Content</TD></TR>
</TABLE>""")
```

### DOT HTML Tags

DOT supports a subset of HTML:

- **Text formatting**: `<B>`, `<I>`, `<U>`, `<S>`
- **Font control**: `<FONT POINT-SIZE="..." COLOR="..." FACE="...">`
- **Layout**: `<TABLE>`, `<TR>`, `<TD>` with attributes
- **Line breaks**: `<BR/>`

## Installation

The HTMLNode feature requires `mistune` for markdown support:

```bash
pip install 'dotspy[html]'
# or
pip install mistune>=3.0
```

If you only use raw HTML mode, `mistune` is not required.

## Usage with Styles

HTMLNode supports all standard Node features:

```python
import dotspy as ds

style = ds.NodeStyle(shape="box", fillcolor="lightblue", style="filled")

with ds.Graph() as g:
    n1 = ds.HTMLNode(
        markdown="**Important**",
        styles=style,
        color="red",
        penwidth=2
    )
```

## Examples

See `examples/html_node_example.py` for more detailed examples.

## API Reference

```python
class HTMLNode(Node):
    def __init__(
        self,
        name: Optional[str] = None,
        markdown: Optional[str] = None,  # Markdown text (mutually exclusive with html)
        html: Optional[str] = None,      # Raw DOT HTML (mutually exclusive with markdown)
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs  # Additional node attributes
    )
```

### Parameters

- **name**: Unique identifier (auto-generated if not provided)
- **markdown**: Markdown text to convert to DOT HTML
- **html**: Raw DOT-compatible HTML
- **styles**: NodeStyle or list of styles to apply
- **attrs**: Additional Graphviz attributes

### Raises

- `ValueError`: If both `markdown` and `html` are provided, or neither is provided
- `ImportError`: If `markdown` is provided but `mistune` is not installed

