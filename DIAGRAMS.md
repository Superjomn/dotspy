# Diagrams Module

This document describes the diagrams module implementation for dotspy, which provides specialized components for common diagram scenarios.

## Overview

The `diagrams` module extends dotspy with domain-specific abstractions for:
- **UML Class Diagrams** - Object-oriented design diagrams
- **Mind Maps** - Hierarchical thought organization

## Classical DOT Scenarios

DOT/Graphviz supports many classical diagram types. This implementation focuses on:

1. **UML Class Diagrams** ✓ Implemented
   - Class nodes with compartments
   - Interface and abstract class support
   - Relationship edges (inheritance, composition, etc.)

2. **Mind Maps** ✓ Implemented
   - Hierarchical topic organization
   - Radial and left-right layouts
   - Helper functions for quick creation

3. **Future Scenarios** (Not yet implemented)
   - Flowcharts - Process flow diagrams
   - State Machines - FSM transitions
   - Entity-Relationship Diagrams - Database schemas
   - Organization Charts - Hierarchical structures
   - Network Diagrams - System architecture
   - Dependency Graphs - Module dependencies

## Architecture

```
dotspy/
  diagrams/
    __init__.py       # Public API exports
    base.py           # Base classes (DiagramNode, DiagramEdge)
    uml.py            # UML class diagram components
    mindmap.py        # Mind map components
```

### Key Design Decisions

1. **Separate Module**: Diagrams live in `dotspy.diagrams` to keep the core API clean
2. **Inheritance Pattern**: Diagram-specific nodes inherit from core `Node` class
3. **Style Templates**: Edge types are style templates applied via `|` operator
4. **Helper Functions**: Provide quick creation for common patterns (e.g., `mindmap()`)

## UML Class Diagrams

### Nodes

#### ClassNode
Creates a class box with compartments for attributes and methods.

```python
ClassNode(
    class_name: str,
    attributes: List[str] = None,
    methods: List[str] = None,
    stereotype: str = None,
    **attrs
)
```

Example:
```python
animal = ClassNode(
    "Animal",
    attributes=["+ name: str", "- age: int"],
    methods=["+ speak(): void", "+ move(): void"]
)
```

#### InterfaceNode
Creates an interface with `<<interface>>` stereotype.

```python
InterfaceNode(
    interface_name: str,
    methods: List[str] = None,
    **attrs
)
```

#### AbstractClassNode
Creates an abstract class with `<<abstract>>` stereotype.

### Edges

All UML edges are used as style templates with the `|` operator:

```python
class1 >> class2 | InheritanceEdge()
```

#### Edge Types

- **InheritanceEdge**: Hollow arrow for "extends" relationships
- **ImplementsEdge**: Dashed hollow arrow for interface implementation
- **CompositionEdge**: Filled diamond for strong ownership
- **AggregationEdge**: Hollow diamond for weak ownership
- **AssociationEdge**: Simple line with optional multiplicity labels
- **DependencyEdge**: Dashed arrow for "uses" relationships

### Graph Style

```python
UML_GRAPH = GraphStyle(
    rankdir="TB",        # Top-bottom layout
    splines="ortho",     # Orthogonal routing
    nodesep=0.8,
    ranksep=1.0,
)
```

## Mind Maps

### Nodes

#### TopicNode
Central topic with prominent styling (large, ellipse, bold).

```python
TopicNode(label: str, name: str = None, **attrs)
```

#### BranchNode
Main branch with medium styling (box, rounded, green).

```python
BranchNode(label: str, name: str = None, **attrs)
```

#### LeafNode
Leaf detail with minimal styling (small box, yellow).

```python
LeafNode(label: str, name: str = None, **attrs)
```

### Edges

#### BranchEdge
No-arrow bold lines for organic mind map appearance.

```python
root >> branch | BranchEdge()
```

### Helper Functions

#### mindmap()
Creates mind map from nested dictionary structure.

```python
mindmap({
    "Root": {
        "Branch1": ["Leaf1", "Leaf2"],
        "Branch2": {
            "SubBranch": ["Leaf3"]
        }
    }
})
```

#### radial_mindmap()
Creates radial layout mind map using twopi engine.

### Graph Styles

```python
MINDMAP_GRAPH = GraphStyle(
    rankdir="LR",
    splines="curved",
    nodesep=0.6,
    ranksep=1.2,
)

RADIAL_MINDMAP_GRAPH = GraphStyle(
    layout="twopi",      # Radial layout
    splines="curved",
    ranksep=2.0,
)
```

## Testing Strategy

All diagram components are tested with:

1. **Unit Tests**: Verify node/edge creation and attributes
2. **DOT Validation**: Check generated DOT syntax
3. **End-to-End Tests**: Verify graphviz can render the output
4. **Integration Tests**: Test interaction with core dotspy features

Test file: `tests/test_diagrams.py` (22 tests)

### Running Tests

```bash
# Run all tests
pytest tests/

# Run only diagram tests
pytest tests/test_diagrams.py -v
```

## Usage Examples

### Complete UML Diagram

```python
from dotspy import Graph
from dotspy.diagrams import (
    ClassNode, InterfaceNode,
    InheritanceEdge, ImplementsEdge,
    UML_GRAPH
)

with Graph("animal_hierarchy", styles=UML_GRAPH) as g:
    # Interface
    drawable = InterfaceNode("Drawable", methods=["+ draw(): void"])

    # Abstract class
    animal = ClassNode(
        "Animal",
        attributes=["# name: str"],
        methods=["+ speak(): void"]
    )

    # Concrete classes
    dog = ClassNode("Dog", methods=["+ bark(): void", "+ draw(): void"])
    cat = ClassNode("Cat", methods=["+ meow(): void", "+ draw(): void"])

    # Relationships
    dog >> animal | InheritanceEdge()
    cat >> animal | InheritanceEdge()
    dog >> drawable | ImplementsEdge()
    cat >> drawable | ImplementsEdge()

    g.render("animals.png")
```

### Complete Mind Map

```python
from dotspy import Graph
from dotspy.diagrams import mindmap, MINDMAP_GRAPH

with Graph("learning_plan", styles=MINDMAP_GRAPH) as g:
    mindmap({
        "Software Development": {
            "Languages": {
                "Python": ["Django", "FastAPI"],
                "JavaScript": ["React", "Node.js"]
            },
            "Databases": ["PostgreSQL", "MongoDB"],
            "DevOps": ["Docker", "Kubernetes", "CI/CD"]
        }
    })

    g.render("learning_plan.png")
```

## Future Extensions

To add new diagram types:

1. Create a new file in `dotspy/diagrams/` (e.g., `flowchart.py`)
2. Define specialized nodes inheriting from `DiagramNode`
3. Define edge style templates inheriting from `DiagramEdge`
4. Create a `GraphStyle` preset
5. Add helper functions if applicable
6. Export from `diagrams/__init__.py`
7. Add comprehensive tests
8. Update documentation

Example structure for flowcharts:

```python
# dotspy/diagrams/flowchart.py
from .base import DiagramNode, DiagramEdge

class ProcessNode(DiagramNode):
    """Rectangle for process steps."""
    pass

class DecisionNode(DiagramNode):
    """Diamond for decisions."""
    pass

class FlowEdge(DiagramEdge):
    """Directed flow edge."""
    pass

FLOWCHART_GRAPH = GraphStyle(rankdir="TB", splines="ortho")
```

## API Stability

The diagrams module API is considered stable for:
- Node and edge class names
- Constructor parameters
- Graph style constants

Internal implementation details may change between versions.
