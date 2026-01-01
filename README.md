# dotspy

A Pythonic wrapper for Graphviz DOT language with CSS-like styling support.

## Features

- **Context Managers**: Clean syntax for defining graphs, subgraphs, and applying styles
- **Operator Overloading**: Use `>>` for edge creation (`node1 >> node2`)
- **Styling**: reusable style objects that can be merged and applied via context managers
- **Built-in Constants**: Autocompletion-friendly constants for shapes, colors, and attributes
- **Jupyter Integration**: Automatic rendering in Jupyter notebooks (SVG and PNG support)
- **Markdown/HTML Labels**: Support for markdown and HTML-like labels in nodes
- **Output**: Render to DOT string, file (PNG, PDF, etc.), or SVG string

## Installation

```bash
pip install dotspy
```

(Requires Graphviz to be installed on your system for rendering)

## Usage

### Basic Example

```python
from dotspy import Graph, Node, LR_GRAPH, BOX_NODE

with Graph("my_graph", style=LR_GRAPH) as g:
    start = Node("start", style=BOX_NODE, label="Start Here")
    end = Node("end", shape="circle", color="red")

    start >> end

    print(g.to_dot())
    g.render("output.png")
```

### Advanced Styling

```python
from dotspy import Graph, Node, NodeStyle, EdgeStyle, RED, BLUE, BOLD

my_node_style = NodeStyle(fontname="Helvetica", fontsize=12)
error_style = NodeStyle(color=RED, style="filled", fillcolor="#ffcccc")

with Graph() as g:
    # Apply default style for this block
    with my_node_style:
        a = Node("A")
        b = Node("B")

    # Override with specific style
    c = Node("C", nstyle=error_style)

    # Using | operator with EdgeStyle
    b >> c | EdgeStyle(style=BOLD, color=RED)

    # Chaining edges
    a >> b >> c | EdgeStyle(color="green", penwidth=2)

    g.render("styled.png")
```

### Subgraphs and Clusters

```python
from dotspy import Graph, Subgraph, TB_GRAPH

with Graph(style=TB_GRAPH) as g:
    start = Node("Start")
    end = Node("End")

    with Subgraph("cluster_process", label="Main Process", bgcolor="lightgrey") as sub:
        step1 = Node("Step 1")
        step2 = Node("Step 2")

        step1 >> step2

    start >> step1
    step2 >> end

    print(g.to_dot())
```

### Jupyter Notebook Support

Graphs automatically render as SVG or PNG in Jupyter notebooks:

```python
from dotspy import Graph, Node

with Graph() as g:
    Node("A") >> Node("B") >> Node("C")

# Just reference the graph object to see it rendered
g  # Displays inline in Jupyter
```

### HTML-like Labels

Use `HTMLNode` for rich formatting with markdown or raw HTML:

```python
from dotspy import Graph, HTMLNode

with Graph() as g:
    # Markdown support
    n1 = HTMLNode(markdown="**Bold** and *Italic*")
    n2 = HTMLNode(markdown="# Header\n- Item 1\n- Item 2")

    # Raw HTML for tables and complex formatting
    n3 = HTMLNode(html="""<TABLE BORDER="1" CELLBORDER="1">
        <TR><TD><B>Header 1</B></TD><TD><B>Header 2</B></TD></TR>
        <TR><TD>Data 1</TD><TD>Data 2</TD></TR>
    </TABLE>""")

    n1 >> n2 >> n3
    g.render("output.png")
```

## Diagram Scenarios

The `diagrams` module provides specialized components for common diagram types:

### UML Class Diagrams

Create professional UML class diagrams with specialized nodes and edges:

```python
from dotspy import Graph
from dotspy.diagrams import (
    ClassNode, InterfaceNode, InheritanceEdge,
    CompositionEdge, UML_GRAPH
)

with Graph("uml", styles=UML_GRAPH) as g:
    # Define classes with attributes and methods
    animal = ClassNode(
        "Animal",
        attributes=["+ name: str", "- age: int"],
        methods=["+ speak(): void"]
    )

    dog = ClassNode(
        "Dog",
        methods=["+ bark(): void"]
    )

    # Interfaces
    drawable = InterfaceNode("Drawable", methods=["+ draw(): void"])

    # Relationships
    dog >> animal | InheritanceEdge()  # Inheritance
    dog >> drawable | ImplementsEdge()  # Interface implementation

    g.render("uml.png")
```

### PlantUML Syntax Support

You can also define nodes using PlantUML syntax for a more concise definition:

```python
from dotspy import Graph
from dotspy.diagrams import create_node, InheritanceEdge, UML_GRAPH

with Graph("uml_puml", styles=UML_GRAPH) as g:
    # Define a class using PlantUML syntax
    user = create_node("""
    class User {
        + name: str
        + email: str
        + login(): void
    }
    """)

    # Define an interface
    drawable = create_node("""
    interface Drawable {
        + draw(): void
    }
    """)

    # Mix with standard Python API
    user >> drawable | InheritanceEdge()  # Just for example
```

**Available UML Components:**
- Nodes: `ClassNode`, `InterfaceNode`, `AbstractClassNode`
- Edges: `InheritanceEdge`, `ImplementsEdge`, `CompositionEdge`, `AggregationEdge`, `AssociationEdge`, `DependencyEdge`
- Style: `UML_GRAPH`

### Mind Maps

Create mind maps with an intuitive object-oriented API:

```python
from dotspy import Graph
import dotspy.diagrams.mindmap as mm

with Graph("ideas", styles=mm.MINDMAP_GRAPH) as g:
    project = mm.MindNode("Project Ideas")
    frontend = mm.MindNode("Frontend")
    backend = mm.MindNode("Backend")
    database = mm.MindNode("Database")

    # Use tuple fan-out to create multiple edges at once
    project >> (frontend, backend, database) | mm.BranchEdge()

    # Chain and fan-out in one expression
    frontend >> (mm.MindNode("React"), mm.MindNode("Vue"), mm.MindNode("Angular"))
    backend >> (mm.MindNode("Django"), mm.MindNode("FastAPI"))
    database >> (mm.MindNode("PostgreSQL"), mm.MindNode("MongoDB"))

    # Add notes/annotations
    note = mm.NoteNode("Focus on TypeScript")
    frontend >> note  # Automatically applies NoteEdge styling

    g.render("mindmap.png")
```

Apply preset styles for visual hierarchy:

```python
from dotspy.diagrams import MindNode, TOPIC_STYLE, BRANCH_STYLE, LEAF_STYLE

# Use preset styles to differentiate node levels
root = MindNode("Central Idea", styles=TOPIC_STYLE)
branch = MindNode("Main Topic", styles=BRANCH_STYLE)
leaf = MindNode("Detail", styles=LEAF_STYLE)
```

**Available Mind Map Components:**
- Nodes: `MindNode`, `NoteNode` (backward compatible: `TopicNode`, `BranchNode`, `LeafNode`)
- Edges: `BranchEdge`, `NoteEdge`
- Styles: `MINDMAP_GRAPH`, `RADIAL_MINDMAP_GRAPH`
- Style Presets: `TOPIC_STYLE`, `BRANCH_STYLE`, `LEAF_STYLE`

## More Examples

See the [examples/](examples/) directory for more complex use cases, including:
- `diagrams_example.py` - Complete UML and mind map examples
- `quickstart.ipynb` - Jupyter notebook with interactive examples

## License

MIT
