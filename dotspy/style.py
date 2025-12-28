from typing import Any, Dict, Optional, List, Union
from pydantic import BaseModel, ConfigDict, PrivateAttr
from .context import push_node_style, pop_node_style, push_edge_style, pop_edge_style
from .attributes import NodeAttributes, EdgeAttributes, GraphAttributes

class BaseStyle(BaseModel):
    """Base class for all styles using Pydantic."""
    
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    _token: Any = PrivateAttr(default=None)

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __enter__(self):
        # Push style to context
        pass
    
    def __exit__(self, *args):
        # Pop style from context
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)
    
    def merge(self, other: "BaseStyle") -> "BaseStyle":
        """Merge another style into this one (other takes precedence)."""
        new_attrs = self.to_dict()
        new_attrs.update(other.to_dict())
        return self.__class__(**new_attrs)

class NodeStyle(BaseStyle, NodeAttributes):
    """Style for nodes."""
    
    def __enter__(self):
        self._token = push_node_style(self)
        return self
    
    def __exit__(self, *args):
        if self._token:
            pop_node_style(self._token)

class EdgeStyle(BaseStyle, EdgeAttributes):
    """Style for edges."""
    
    def __enter__(self):
        self._token = push_edge_style(self)
        return self
    
    def __exit__(self, *args):
        if self._token:
            pop_edge_style(self._token)

class GraphStyle(BaseStyle, GraphAttributes):
    """Style for graphs/subgraphs."""
    pass

def merge_styles(styles: Union[BaseStyle, List[BaseStyle], None]) -> Dict[str, Any]:
    """Merge multiple styles, later styles override earlier ones."""
    if styles is None:
        return {}
    if isinstance(styles, BaseStyle):
        return styles.to_dict()
    
    # List of styles - merge in order
    merged = {}
    if isinstance(styles, list):
        for style in styles:
            if style:  # Handle potential None in list or just being safe
                merged.update(style.to_dict())
    return merged
