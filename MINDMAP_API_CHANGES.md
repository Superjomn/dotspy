# MindMap API Redesign - Summary of Changes

## Overview

The MindMap module has been redesigned to provide a more consistent, object-oriented API that aligns with dotspy's core Node and Edge patterns. The new design removes the dictionary-based helper functions in favor of explicit node creation and tuple fan-out syntax.

## Key Changes

### 1. Unified Node Class: `MindNode`

**Before:**
```python
from dotspy.diagrams import TopicNode, BranchNode, LeafNode

root = TopicNode("Project")
branch = BranchNode("Frontend")
leaf = LeafNode("React")
```

**After:**
```python
import dotspy.diagrams.mindmap as mm

root = mm.MindNode("Project")
branch = mm.MindNode("Frontend")
leaf = mm.MindNode("React")

# Optional: Apply preset styles
root = mm.MindNode("Project", styles=mm.TOPIC_STYLE)
branch = mm.MindNode("Frontend", styles=mm.BRANCH_STYLE)
leaf = mm.MindNode("React", styles=mm.LEAF_STYLE)
```

### 2. New Annotation Support: `NoteNode`

```python
note = mm.NoteNode("Important detail")
note.attach_to(some_node)  # Creates a dashed edge to the node
```

### 3. Tuple Fan-out Syntax

**Before:**
```python
root >> branch1 | BranchEdge()
root >> branch2 | BranchEdge()
root >> branch3 | BranchEdge()
```

**After:**
```python
root >> (branch1, branch2, branch3) | mm.BranchEdge()

# Or inline:
root >> (mm.MindNode("A"), mm.MindNode("B"), mm.MindNode("C"))
```

### 4. Removed Helper Functions

The `mindmap()` and `radial_mindmap()` dictionary-based helper functions have been removed. Users should now create nodes explicitly.

**Before:**
```python
from dotspy.diagrams import mindmap

mindmap({
    "Project": {
        "Frontend": ["React", "Vue"],
        "Backend": ["Django", "Flask"]
    }
})
```

**After:**
```python
import dotspy.diagrams.mindmap as mm

project = mm.MindNode("Project")
frontend = mm.MindNode("Frontend")
backend = mm.MindNode("Backend")

project >> (frontend, backend) | mm.BranchEdge()
frontend >> (mm.MindNode("React"), mm.MindNode("Vue"))
backend >> (mm.MindNode("Django"), mm.MindNode("Flask"))
```

## Backward Compatibility

- `TopicNode`, `BranchNode`, and `LeafNode` are still available as aliases to `MindNode` for backward compatibility
- All existing edge types (`BranchEdge`) remain unchanged
- Graph styles (`MINDMAP_GRAPH`, `RADIAL_MINDMAP_GRAPH`) remain unchanged
- Style presets (`TOPIC_STYLE`, `BRANCH_STYLE`, `LEAF_STYLE`) are still available

## New Components

- **`MindNode`**: Unified node class for all mind map nodes
- **`NoteNode`**: Specialized node for annotations that auto-applies NoteEdge styling when used with `>>`
- **`NoteEdge`**: Dashed edge style for connecting notes (automatically applied to NoteNode targets)

## Complete Example

```python
from dotspy import Graph
import dotspy.diagrams.mindmap as mm

with Graph("ideas", styles=mm.MINDMAP_GRAPH) as g:
    # Create nodes
    project = mm.MindNode("Project Ideas", styles=mm.TOPIC_STYLE)
    frontend = mm.MindNode("Frontend", styles=mm.BRANCH_STYLE)
    backend = mm.MindNode("Backend", styles=mm.BRANCH_STYLE)

    # Create edges with tuple fan-out
    project >> (frontend, backend) | mm.BranchEdge()

    # Fan out to multiple leaf nodes
    frontend >> (
        mm.MindNode("React", styles=mm.LEAF_STYLE),
        mm.MindNode("Vue", styles=mm.LEAF_STYLE),
        mm.MindNode("Angular", styles=mm.LEAF_STYLE),
    )

    # Add a note
    note = mm.NoteNode("Focus on TypeScript")
    frontend >> note  # Automatically applies NoteEdge styling

    g.render("mindmap.png")
```

## Migration Guide

### Simple Migration

If you were using `TopicNode`, `BranchNode`, `LeafNode` directly, your code will continue to work without changes due to backward compatibility aliases.

### Full Migration

To adopt the new API:

1. Replace `TopicNode`, `BranchNode`, `LeafNode` with `MindNode`
2. Apply style presets explicitly if you want different visual styles
3. Use tuple fan-out syntax to simplify multiple edge creation
4. Remove any usage of `mindmap()` or `radial_mindmap()` helper functions

## Benefits

1. **Consistency**: MindMap nodes now work exactly like other dotspy nodes
2. **Flexibility**: Single node class with optional styling is more flexible
3. **Expressiveness**: Tuple fan-out syntax is more concise and readable
4. **Extensibility**: Easier to add new node types (like `NoteNode`)
5. **Type Safety**: Explicit node creation is easier to type-check

## Files Modified

- `dotspy/node.py`: Added tuple fan-out support to `Node.__rshift__`
- `dotspy/edge.py`: Added tuple fan-out support to `Edge.__rshift__` and `EdgeChain.__rshift__`
- `dotspy/diagrams/mindmap.py`: Complete rewrite with new API
- `dotspy/diagrams/__init__.py`: Updated exports
- `dotspy/__init__.py`: Updated exports
- `tests/test_diagrams.py`: Updated all mind map tests
- `README.md`: Updated documentation
- `examples/mindmap_new_api.py`: New example file
