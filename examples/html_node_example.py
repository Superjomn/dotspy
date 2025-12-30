"""
Example demonstrating HTMLNode functionality.

HTMLNode allows you to create nodes with HTML-like labels in two ways:
1. Markdown mode: Provide markdown text that gets converted to DOT HTML
2. Raw HTML mode: Provide raw DOT-compatible HTML directly
"""

import dotspy as ds

# Example 1: Using raw HTML
print("Example 1: Raw HTML")
print("-" * 50)
with ds.Graph(label="Raw HTML Example", rankdir=ds.LR) as g:
    n1 = ds.HTMLNode(name="raw1", html="<B>Bold</B> text")
    n2 = ds.HTMLNode(name="raw2", html="<I>Italic</I> text")
    n3 = ds.HTMLNode(name="raw3", html='<FONT POINT-SIZE="16" COLOR="red">Large Red</FONT>')
    n1 >> n2 >> n3

print(g.to_dot())
print()

# Example 2: Using markdown
print("Example 2: Markdown")
print("-" * 50)
with ds.Graph(label="Markdown Example", rankdir=ds.LR) as g:
    n1 = ds.HTMLNode(name="md1", markdown="**Bold** text")
    n2 = ds.HTMLNode(name="md2", markdown="*Italic* text")
    n3 = ds.HTMLNode(name="md3", markdown="~~Strikethrough~~")
    n1 >> n2 >> n3

print(g.to_dot())
print()

# Example 3: Markdown with headers
print("Example 3: Markdown Headers")
print("-" * 50)
with ds.Graph(label="Headers Example", rankdir=ds.TB) as g:
    n1 = ds.HTMLNode(markdown="# Main Title")
    n2 = ds.HTMLNode(markdown="## Subtitle")
    n3 = ds.HTMLNode(markdown="### Section")
    n1 >> n2 >> n3

print(g.to_dot())
print()

# Example 4: Complex HTML with tables
print("Example 4: HTML Tables")
print("-" * 50)
with ds.Graph(label="Table Example") as g:
    table_html = """<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
  <TR><TD><B>Header 1</B></TD><TD><B>Header 2</B></TD></TR>
  <TR><TD>Data 1</TD><TD>Data 2</TD></TR>
</TABLE>"""
    
    n1 = ds.HTMLNode(name="table", html=table_html)
    n2 = ds.Node("normal", label="Regular Node")
    n1 >> n2

print(g.to_dot())
print()

# Example 5: Markdown lists
print("Example 5: Markdown Lists")
print("-" * 50)
with ds.Graph(label="List Example") as g:
    markdown_list = """# Task List

- Item 1
- Item 2
- Item 3"""
    
    n1 = ds.HTMLNode(markdown=markdown_list)

print(g.to_dot())
print()

# Example 6: Mixed formatting with markdown
print("Example 6: Mixed Formatting")
print("-" * 50)
with ds.Graph(label="Mixed Example") as g:
    mixed = """**Important:** This is *really* important

See documentation"""
    
    n1 = ds.HTMLNode(markdown=mixed)
    n2 = ds.Node("action", label="Take Action")
    n1 >> n2

print(g.to_dot())
print()

# Example 7: HTMLNode with styles
print("Example 7: HTMLNode with Styles")
print("-" * 50)
with ds.Graph(label="Styled HTML Example") as g:
    style = ds.NodeStyle(shape="box", fillcolor="lightblue", style="filled")
    n1 = ds.HTMLNode(markdown="**Styled** Node", styles=style)
    n2 = ds.HTMLNode(html="<I>Another</I> <B>Styled</B> Node", 
                     styles=style, color="red", penwidth=2)
    n1 >> n2

print(g.to_dot())

