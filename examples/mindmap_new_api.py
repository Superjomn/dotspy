"""Example demonstrating the new MindMap API."""

import dotspy.diagrams.mindmap as mm
from dotspy import Graph

# Example 1: Basic mind map with tuple fan-out
with Graph("project_ideas", styles=mm.MINDMAP_GRAPH) as g:
    project = mm.MindNode("Project Ideas")
    frontend = mm.MindNode("Frontend")
    backend = mm.MindNode("Backend")
    database = mm.MindNode("Database")

    # Create edges to multiple nodes using tuple fan-out
    project >> (frontend, backend, database) | mm.BranchEdge()

    # Fan out from frontend
    frontend >> (
        mm.MindNode("React"),
        mm.MindNode("Vue"),
        mm.MindNode("Angular"),
    ) | mm.BranchEdge()

    # Fan out from backend
    backend >> (
        mm.MindNode("Django"),
        mm.MindNode("FastAPI"),
        mm.MindNode("Flask"),
    ) | mm.BranchEdge()

    # Fan out from database
    database >> (
        mm.MindNode("PostgreSQL"),
        mm.MindNode("MongoDB"),
    ) | mm.BranchEdge()

    # Add a note
    note = mm.NoteNode("Focus on modern frameworks")
    frontend >> note  # Automatically applies NoteEdge styling

    g.render("mindmap_new_api.png")
    print("Generated: mindmap_new_api.png")


# Example 2: Using style presets
with Graph("styled_mindmap", styles=mm.MINDMAP_GRAPH) as g:
    # Use TOPIC_STYLE for the root
    root = mm.MindNode("Learning Path", styles=mm.TOPIC_STYLE)

    # Use BRANCH_STYLE for main branches
    basics = mm.MindNode("Basics", styles=mm.BRANCH_STYLE)
    advanced = mm.MindNode("Advanced", styles=mm.BRANCH_STYLE)

    root >> (basics, advanced) | mm.BranchEdge()

    # Use LEAF_STYLE for leaf nodes
    basics >> (
        mm.MindNode("Variables", styles=mm.LEAF_STYLE),
        mm.MindNode("Functions", styles=mm.LEAF_STYLE),
        mm.MindNode("Classes", styles=mm.LEAF_STYLE),
    ) | mm.BranchEdge()

    advanced >> (
        mm.MindNode("Decorators", styles=mm.LEAF_STYLE),
        mm.MindNode("Generators", styles=mm.LEAF_STYLE),
        mm.MindNode("Async/Await", styles=mm.LEAF_STYLE),
    ) | mm.BranchEdge()

    g.render("styled_mindmap.png")
    print("Generated: styled_mindmap.png")


# Example 3: Radial layout
with Graph("radial", styles=mm.RADIAL_MINDMAP_GRAPH) as g:
    center = mm.MindNode("AI Technologies", styles=mm.TOPIC_STYLE)

    center >> (
        mm.MindNode("Machine Learning"),
        mm.MindNode("Deep Learning"),
        mm.MindNode("NLP"),
        mm.MindNode("Computer Vision"),
        mm.MindNode("Robotics"),
    ) | mm.BranchEdge()

    g.render("radial_mindmap.png")
    print("Generated: radial_mindmap.png")
