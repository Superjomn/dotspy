from dotspy import Graph, Node, Subgraph


def test_nested_subgraphs():
    with Graph("G") as g:
        with Subgraph("s1") as s1:
            n1 = Node("n1")
            with Subgraph("s2") as s2:
                n2 = Node("n2")

    dot = g.to_dot()
    # Check structure by indentation or direct substring matching
    # s2 should be inside s1
    # This means "subgraph "cluster_s2" {" should appear AFTER "subgraph "cluster_s1" {"
    # AND before the closing brace of s1.

    # Simple check: verify s2 is not a direct child of G (if indentation allows checking)
    # or check that s2 definition is between s1 start and s1 end.

    s1_start = dot.find('subgraph "cluster_s1" {')
    s2_start = dot.find('subgraph "cluster_s2" {')

    assert s1_start != -1
    assert s2_start != -1
    assert s2_start > s1_start, "s2 should start after s1"

    # Find closing brace of s1 is harder without parsing, but we can assume
    # if it was flattened, s1 closing brace would be before s2 start.
    # However, standard renderer puts all subgraphs at top level if not nested.
    # If flattened:
    # subgraph s1 { ... }
    # subgraph s2 { ... }
    # Then s2_start > s1_start is true.
    # We need to verify s2 is INSIDE s1.

    # If we inspect the object model:
    # s1 should have s2 in its subgraphs (once implemented)
    # g should NOT have s2 in its subgraphs directly (only s1)

    # For now, let's just assert the failure of current implementation
    # Current implementation: both s1 and s2 are in g._subgraphs
    assert (
        len(g._subgraphs) == 1
    ), f"Graph should have 1 top-level subgraph, found {len(g._subgraphs)}"
    # This assertion will fail before fix
