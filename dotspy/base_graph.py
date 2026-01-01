import sys
from typing import Callable, Dict, List, Optional

from .graph import Subgraph
from .node import Node


class BaseGraph:
    """
    Base class for declarative node grouping.

    Allows defining groups of nodes using methods decorated with @BaseGraph.add_node.
    Can optionally wrap these nodes in a Subgraph or just act as a container.

    Example:
        class AppGraph(BaseGraph):
            @BaseGraph.add_node
            def _(self):
                return Node("Class0")

            @BaseGraph.add_node
            def _(self):
                return Node("Class1")

        app = AppGraph()
        app.Class0 >> app.Class1
    """

    _node_factories: List[Callable]

    @staticmethod
    def add_node(func: Callable) -> Callable:
        """
        Decorator to mark a method as a node factory.

        Uses frame inspection to register the factory in the class being defined,
        allowing multiple methods with the same name (e.g. _) to be registered.
        """
        func._is_node_factory = True

        # Get the frame of the caller (the class body)
        try:
            frame = sys._getframe(1)
        except ValueError:
            # Fallback if stack depth is insufficient (shouldn't happen in normal class def)
            return func

        locals_dict = frame.f_locals

        # Initialize the list if it doesn't exist in the current class scope
        if "_node_factories" not in locals_dict:
            locals_dict["_node_factories"] = []

        # Append the function
        locals_dict["_node_factories"].append(func)

        return func

    def __init__(
        self,
        label: Optional[str] = None,
        use_subgraph: bool = False,
        **attrs,
    ):
        """
        Initialize the node group.

        Args:
            label: Optional label (used when use_subgraph=True).
            use_subgraph: If True, creates a Subgraph and registers nodes within it.
                         If False, nodes are registered with the currently active context.
            **attrs: Additional attributes passed to Subgraph constructor (if used).
        """
        self._nodes: Dict[str, Node] = {}
        self._subgraph: Optional[Subgraph] = None

        # Setup context if using subgraph
        context = None
        if use_subgraph:
            # If label is not provided, use a default
            name = label if label else "cluster_group"
            self._subgraph = Subgraph(name=name, **attrs)
            context = self._subgraph

        # If we have a subgraph, we need to enter its context so nodes are added to it
        if context:
            with context:
                self._create_nodes()
        else:
            # Otherwise just create nodes (they will find current active graph/subgraph)
            self._create_nodes()

    def _create_nodes(self):
        """Invoke all factory methods to create nodes."""
        factories = self._collect_factories()

        for method in factories:
            # Bind method to self
            # Since method is a function object from the class, we call it with self
            node = method(self)

            if not isinstance(node, Node):
                raise TypeError(
                    f"Factory method {method.__name__} must return a Node instance, got {type(node)}"
                )

            if node.name in self._nodes:
                raise ValueError(f"Duplicate node name found: {node.name}")

            self._nodes[node.name] = node

    def _collect_factories(self) -> List[Callable]:
        """Collect all node factories from the class hierarchy."""
        factories = []

        # Walk MRO in reverse to respect inheritance order (parents first)
        for cls in reversed(self.__class__.mro()):
            # Check if this specific class has factories defined in its __dict__
            # This avoids adding the same list multiple times if it's inherited
            if "_node_factories" in cls.__dict__:
                factories.extend(cls.__dict__["_node_factories"])

        return factories

    def __getattr__(self, name: str) -> Node:
        """Access nodes by name."""
        if name in self._nodes:
            return self._nodes[name]

        # If wrapped in a subgraph, delegate attribute access
        if self._subgraph:
            try:
                return getattr(self._subgraph, name)
            except AttributeError:
                pass

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __enter__(self):
        if self._subgraph:
            return self._subgraph.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._subgraph:
            return self._subgraph.__exit__(exc_type, exc_val, exc_tb)
