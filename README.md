# dotspy

A Pythonic wrapper for Graphviz DOT language with CSS-like styling support.

## Features

- **Context Managers**: Clean syntax for defining graphs, subgraphs, and applying styles
- **Operator Overloading**: Use `>>` for edge creation (`node1 >> node2`)
- **Styling**: reusable style objects that can be merged and applied via context managers
- **Built-in Constants**: Autocompletion-friendly constants for shapes, colors, and attributes
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
    # g.render("output.png")
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
    
    # Edges with styles
    (a >> b).style(color=BLUE)
    
    # Using | operator with dict
    b >> c | {"style": BOLD, "color": RED}

    # Chaining edges
    a >> b >> c | {"color": "green", "penwidth": 2}

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

## License

MIT
