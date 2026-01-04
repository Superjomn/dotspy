import unittest

from dotspy import (
    BLUEPRINT_THEME,
    DARK_THEME,
    DEFAULT_THEME,
    FOREST_THEME,
    MINIMAL_THEME,
    OCEAN_THEME,
    PASTEL_THEME,
    THEMES,
    Graph,
    Node,
    NodeStyle,
    Subgraph,
)
from dotspy.context import get_active_theme


class TestThemes(unittest.TestCase):
    def test_all_themes_exist(self):
        """Test that all built-in themes are registered."""
        expected_themes = [
            "default",
            "dark",
            "pastel",
            "blueprint",
            "forest",
            "ocean",
            "minimal",
        ]
        for theme_name in expected_themes:
            self.assertIn(theme_name, THEMES)

    def test_theme_constants_exported(self):
        """Test that theme constants are exported."""
        self.assertIsNotNone(DEFAULT_THEME)
        self.assertIsNotNone(DARK_THEME)
        self.assertIsNotNone(PASTEL_THEME)
        self.assertIsNotNone(BLUEPRINT_THEME)
        self.assertIsNotNone(FOREST_THEME)
        self.assertIsNotNone(OCEAN_THEME)
        self.assertIsNotNone(MINIMAL_THEME)

    def test_default_theme_applied(self):
        """Test that default theme applies correct styles."""
        with Graph("test", theme="default") as g:
            n = Node("A")
            n2 = Node("B")
            e = n >> n2

            # Check node has theme styles
            self.assertEqual(n.attrs.get("shape"), "box")
            self.assertEqual(n.attrs.get("fillcolor"), "lightblue")
            self.assertIn("filled", n.attrs.get("style", ""))
            self.assertIn("rounded", n.attrs.get("style", ""))

            # Check edge has theme styles
            edge = e.edges[0]
            self.assertEqual(edge.attrs.get("color"), "gray")

            # Check graph has theme styles
            self.assertEqual(g.attrs.get("bgcolor"), "white")

    def test_dark_theme_applied(self):
        """Test that dark theme applies correct styles."""
        with Graph("test", theme="dark") as g:
            n = Node("A")

            # Check dark theme specific attributes
            self.assertEqual(n.attrs.get("fillcolor"), "#4d4d4d")
            self.assertEqual(n.attrs.get("fontcolor"), "white")
            self.assertEqual(g.attrs.get("bgcolor"), "#2d2d2d")

    def test_pastel_theme_applied(self):
        """Test that pastel theme applies correct styles."""
        with Graph("test", theme="pastel") as g:
            n = Node("A")

            # Check pastel theme specific attributes
            self.assertEqual(n.attrs.get("shape"), "ellipse")
            self.assertEqual(n.attrs.get("fillcolor"), "#ffb7b2")
            self.assertEqual(g.attrs.get("bgcolor"), "#fdfbf7")

    def test_blueprint_theme_applied(self):
        """Test that blueprint theme applies correct styles."""
        with Graph("test", theme="blueprint") as g:
            n = Node("A")
            n2 = Node("B")
            e = n >> n2
            edge = e.edges[0]

            # Check blueprint theme specific attributes
            self.assertEqual(n.attrs.get("color"), "white")
            self.assertEqual(n.attrs.get("fontcolor"), "white")
            self.assertEqual(edge.attrs.get("style"), "dashed")
            self.assertEqual(g.attrs.get("bgcolor"), "#1a237e")

    def test_forest_theme_applied(self):
        """Test that forest theme applies correct styles."""
        with Graph("test", theme="forest") as g:
            n = Node("A")
            n2 = Node("B")
            e = n >> n2
            edge = e.edges[0]

            # Check forest theme specific attributes
            self.assertEqual(n.attrs.get("shape"), "circle")
            self.assertEqual(n.attrs.get("fillcolor"), "#a5d6a7")
            self.assertEqual(edge.attrs.get("color"), "#5d4037")

    def test_ocean_theme_applied(self):
        """Test that ocean theme applies correct styles."""
        with Graph("test", theme="ocean") as g:
            n = Node("A")

            # Check ocean theme specific attributes
            self.assertEqual(n.attrs.get("fillcolor"), "#4dd0e1")
            self.assertEqual(g.attrs.get("bgcolor"), "#e0f7fa")

    def test_minimal_theme_applied(self):
        """Test that minimal theme applies correct styles."""
        with Graph("test", theme="minimal") as g:
            n = Node("A")
            n2 = Node("B")
            e = n >> n2
            edge = e.edges[0]

            # Check minimal theme specific attributes
            self.assertEqual(n.attrs.get("style"), "solid")
            self.assertEqual(n.attrs.get("color"), "black")
            self.assertEqual(edge.attrs.get("color"), "black")

    def test_explicit_style_overrides_theme(self):
        """Test that explicit styles parameter overrides theme."""
        custom_style = NodeStyle(fillcolor="red", shape="diamond")

        with Graph("test", theme="default"):
            n = Node("A", styles=custom_style)

            # Custom style should override theme
            self.assertEqual(n.attrs.get("fillcolor"), "red")
            self.assertEqual(n.attrs.get("shape"), "diamond")

    def test_direct_attribute_overrides_theme(self):
        """Test that direct attributes override theme."""
        with Graph("test", theme="default"):
            n = Node("A", fillcolor="purple", fontcolor="yellow")

            # Direct attributes should override theme
            self.assertEqual(n.attrs.get("fillcolor"), "purple")
            self.assertEqual(n.attrs.get("fontcolor"), "yellow")

            # But other theme attributes should still apply
            self.assertEqual(n.attrs.get("shape"), "box")

    def test_nested_subgraph_inherits_theme(self):
        """Test that subgraph without theme inherits parent graph's theme."""
        with Graph("test", theme="dark"):
            # Node in parent graph
            n1 = Node("A")

            with Subgraph("sub"):
                # Node in subgraph should inherit parent's theme
                n2 = Node("B")
                n3 = Node("C")
                e = n2 >> n3
                edge = e.edges[0]

                # Check that nodes in subgraph have dark theme
                self.assertEqual(n2.attrs.get("fillcolor"), "#4d4d4d")
                self.assertEqual(n2.attrs.get("fontcolor"), "white")
                self.assertEqual(edge.attrs.get("color"), "lightgray")

            # Verify parent node also has theme
            self.assertEqual(n1.attrs.get("fillcolor"), "#4d4d4d")

    def test_subgraph_own_theme_overrides_parent(self):
        """Test that subgraph with its own theme overrides parent's theme."""
        with Graph("test", theme="dark"):
            # Node in parent graph with dark theme
            n1 = Node("A")
            self.assertEqual(n1.attrs.get("fillcolor"), "#4d4d4d")

            with Subgraph("sub", theme="pastel"):
                # Node in subgraph should have pastel theme
                n2 = Node("B")
                self.assertEqual(n2.attrs.get("fillcolor"), "#ffb7b2")
                self.assertEqual(n2.attrs.get("shape"), "ellipse")

            # Node created after subgraph should have dark theme again
            n3 = Node("C")
            self.assertEqual(n3.attrs.get("fillcolor"), "#4d4d4d")

    def test_theme_context_cleanup(self):
        """Test that theme context is properly cleaned up."""
        # Initially no theme
        self.assertIsNone(get_active_theme())

        with Graph("test", theme="default"):
            # Theme is active inside context
            self.assertIsNotNone(get_active_theme())
            self.assertEqual(get_active_theme().name, "default")

        # Theme is cleaned up after exiting
        self.assertIsNone(get_active_theme())

    def test_nested_theme_context_cleanup(self):
        """Test that nested themes are properly cleaned up."""
        with Graph("test", theme="dark"):
            self.assertEqual(get_active_theme().name, "dark")

            with Subgraph("sub", theme="pastel"):
                # Inner theme overrides
                self.assertEqual(get_active_theme().name, "pastel")

            # Outer theme is restored
            self.assertEqual(get_active_theme().name, "dark")

        # All themes cleaned up
        self.assertIsNone(get_active_theme())

    def test_multiple_nested_subgraphs_with_themes(self):
        """Test multiple levels of nested subgraphs with different themes."""
        with Graph("test", theme="default"):
            n1 = Node("A")
            self.assertEqual(n1.attrs.get("fillcolor"), "lightblue")

            with Subgraph("sub1", theme="dark"):
                n2 = Node("B")
                self.assertEqual(n2.attrs.get("fillcolor"), "#4d4d4d")

                with Subgraph("sub2", theme="forest"):
                    n3 = Node("C")
                    self.assertEqual(n3.attrs.get("fillcolor"), "#a5d6a7")
                    self.assertEqual(n3.attrs.get("shape"), "circle")

                # Back to dark theme
                n4 = Node("D")
                self.assertEqual(n4.attrs.get("fillcolor"), "#4d4d4d")

            # Back to default theme
            n5 = Node("E")
            self.assertEqual(n5.attrs.get("fillcolor"), "lightblue")

    def test_theme_applies_to_edges_in_subgraph(self):
        """Test that theme applies to edges created in subgraph."""
        with Graph("test", theme="blueprint"):
            n1 = Node("A")

            with Subgraph("sub", theme="forest"):
                n2 = Node("B")
                n3 = Node("C")
                e = n2 >> n3
                edge = e.edges[0]

                # Edge should have forest theme
                self.assertEqual(edge.attrs.get("color"), "#5d4037")

    def test_invalid_theme_name_ignored(self):
        """Test that invalid theme name doesn't crash."""
        # Should not crash, just ignore the invalid theme
        with Graph("test", theme="nonexistent") as g:
            n = Node("A")
            # Node won't have theme styles since theme doesn't exist
            # Just verify it doesn't crash


if __name__ == "__main__":
    unittest.main()
