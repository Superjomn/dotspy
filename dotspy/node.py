from typing import Any, Dict, Optional, TYPE_CHECKING, ClassVar, List, Union
from pydantic import Field, PrivateAttr, ConfigDict
from .context import get_active_node_styles, get_current_subgraph, get_current_graph, get_graph
from .attributes import NodeAttributes
from .style import NodeStyle, merge_styles

if TYPE_CHECKING:
    from .edge import EdgeBuilder

class Node(NodeAttributes):
    """Represents a graph node."""
    
    # Allow extra fields for arbitrary Graphviz attributes
    # Add explicit ClassVar ignored types or configuration to skip them
    # Note: ignored_types accepts types, not instances. But Pydantic still complains about unannotated attribute.
    # The error says: A non-annotated attribute was detected: `ClassVar = typing.ClassVar`.
    # Wait, my import statement was `from typing import ClassVar`.
    # And then I used `_id_counter: ClassVar[int] = 0`.
    # The error message `ClassVar = typing.ClassVar` suggests that the import itself is being inspected 
    # and considered as an unannotated attribute if it's inside the class?
    # No, the import is at module level or inside the class? 
    # Ah, I put the import INSIDE the class body in my previous edit!
    # Imports inside class body are treated as class attributes.
    # I must move the import to top level.
    
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    name: str = Field(..., description="Unique identifier for the node.")
    
    # Internal state
    _attrs: Dict[str, Any] = PrivateAttr(default_factory=dict)
    
    def __init__(
        self,
        name: Optional[str] = None,
        styles: Optional[Union[NodeStyle, List[NodeStyle]]] = None,
        **attrs
    ):
        # Generate unique ID if name not provided
        # Since 'name' is required by Pydantic model, we generate it before super().__init__
        if name is None:
            name = self._generate_name()
            
        # Merge active context styles
        context_attrs = {}
        for ctx_style in get_active_node_styles():
            context_attrs.update(ctx_style.to_dict())
            
        # Merge provided style object
        style_attrs = merge_styles(styles)

        # Combine all attributes
        # Priority: Context < Style Object < Direct Attributes
        combined_attrs = {**context_attrs, **style_attrs, **attrs}
        
        # Initialize Pydantic model
        super().__init__(name=name, **combined_attrs)
        
        # Store all attributes (including extras) in _attrs for rendering fallback/easy access
        # Pydantic stores known fields in self.__dict__ or model fields, and extras in __pydantic_extra__
        # But we want a unified view for rendering.
        # We can reconstruct it on demand or maintain _attrs. 
        # For backward compatibility with existing renderer which accesses .attrs property:
        self._attrs = self.model_dump(exclude_none=True, by_alias=True)
        
        # Register with current graph/subgraph
        self._register()
    
    # Class var to track IDs
    _id_counter: ClassVar[int] = 0
    
    @classmethod
    def _generate_name(cls) -> str:
        # Accessing class var is fine
        cls._id_counter += 1
        return f"node_{cls._id_counter}"
    
    def _register(self):
        """Register this node with current subgraph or graph."""
        subgraph = get_current_subgraph()
        if subgraph:
            subgraph._add_node(self)
        else:
            graph = get_current_graph() or get_graph()
            if graph:
                graph._add_node(self)
    
    def __rshift__(self, other: "Node") -> "EdgeBuilder":
        """Support node1 >> node2 syntax."""
        from .edge import Edge, EdgeChain
        return EdgeChain([Edge(self, other)])
    
    @property
    def attrs(self) -> Dict[str, Any]:
        """Return all attributes as a dictionary (for renderer compatibility)."""
        # Return merged dict of model fields and extras
        # Exclude 'name' from attributes dict as it is structural and handled separately by renderer
        return self.model_dump(exclude_none=True, by_alias=True, exclude={'name'})
