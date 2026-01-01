"""PlantUML syntax parser for creating UML nodes."""

import re
from typing import Dict, List, Union

from .uml import AbstractClassNode, ClassNode, InterfaceNode

# Regex patterns for parsing PlantUML class syntax
# Matches: "type name <<stereotype>> {"
# Groups:
# 1. Type (class, abstract class, interface, enum)
# 2. Name
# 3. Stereotype (optional, inside << >>)
# Enforce opening brace
HEADER_PATTERN = re.compile(
    r"^\s*(abstract\s+class|class|interface|enum)\s+(\w+)(?:\s+<<(.+?)>>)?\s*\{",
    re.IGNORECASE,
)

# Matches members inside the class body
# Groups:
# 1. Member line content
MEMBER_PATTERN = re.compile(r"^\s*(.+?)\s*$", re.MULTILINE)


def parse_plantuml_class(puml_def: str) -> Dict[str, Union[str, List[str]]]:
    """
    Parse a PlantUML class definition string.

    Args:
        puml_def: PlantUML class definition string

    Returns:
        Dictionary containing parsed components:
        - type: Node type (class, abstract class, interface, enum)
        - name: Class name
        - stereotype: Stereotype string (optional)
        - attributes: List of attribute strings
        - methods: List of method strings
    """
    lines = [line.strip() for line in puml_def.strip().split("\n") if line.strip()]
    if not lines:
        raise ValueError("Empty PlantUML definition")

    # Parse header
    header_match = HEADER_PATTERN.match(lines[0])
    if not header_match:
        raise ValueError(
            f"Invalid PlantUML class header (must include opening brace): {lines[0]}"
        )

    node_type = header_match.group(1).lower()
    name = header_match.group(2)
    stereotype = header_match.group(3)

    attributes = []
    methods = []

    # Parse body
    # Skip first line (header) and last line if it's just closing brace
    body_lines = lines[1:]
    if body_lines and body_lines[-1] == "}":
        body_lines = body_lines[:-1]

    for line in body_lines:
        # Skip empty lines or closing braces inside body
        if not line or line == "}":
            continue

        # Strip comments
        # 1. Line comments starting with '
        if line.startswith("'"):
            continue

        # 2. Block comments /' ... '/
        # (Simplified handling: assume block comments are on their own lines or we just ignore lines starting with /')
        if line.startswith("/'"):
            continue
        if line.endswith("'/"):
            continue

        # Also handle comments at end of line?
        # line = line.split("'")[0].strip() # This might be too aggressive if ' is in string

        # Check if it's a method (contains parentheses)
        if "(" in line and ")" in line:
            methods.append(line)
        else:
            attributes.append(line)

    return {
        "type": node_type,
        "name": name,
        "stereotype": stereotype,
        "attributes": attributes,
        "methods": methods,
    }


def create_node(
    puml_def: str, **kwargs
) -> Union[ClassNode, InterfaceNode, AbstractClassNode]:
    """
    Create a UML node from a PlantUML syntax definition.

    Supports:
    - class
    - abstract class
    - interface
    - enum

    Args:
        puml_def: PlantUML definition string
        **kwargs: Additional arguments passed to the node constructor

    Returns:
        Appropriate UML node instance (ClassNode, InterfaceNode, etc.)

    Example:
        >>> node = create_node('''
        ...     class User {
        ...         + name: str
        ...         + login(): void
        ...     }
        ... ''')
    """
    parsed = parse_plantuml_class(puml_def)

    node_type = parsed["type"]
    name = parsed["name"]
    stereotype = parsed["stereotype"]
    attributes = parsed["attributes"]
    methods = parsed["methods"]

    # Handle explicit stereotype override from kwargs
    if "stereotype" in kwargs:
        stereotype = kwargs.pop("stereotype")

    if node_type == "interface":
        return InterfaceNode(
            interface_name=name,
            methods=methods,
            **kwargs,
        )

    elif node_type == "abstract class":
        # Don't pass stereotype="abstract" explicitly as AbstractClassNode handles it
        # UNLESS it was overridden by kwargs or parsed from puml

        if stereotype and stereotype != "abstract":
            # If parsed from puml (e.g. abstract class A <<custom>>)
            # AbstractClassNode doesn't accept stereotype in __init__, so we can't easily override it
            # without modifying AbstractClassNode or hacking.
            # But ClassNode uses it.
            # Wait, AbstractClassNode calls super().__init__(..., stereotype="abstract", ...)
            # So if we pass stereotype in **kwargs/attrs, it will crash with "multiple values"

            # The only way to support custom stereotype on AbstractClassNode is if AbstractClassNode
            # allows overriding it. It currently doesn't.
            # So we ignore the parsed stereotype for abstract classes if it differs,
            # or we implement it by creating ClassNode(..., styles=[UML_ABSTRACT_STYLE]) manually?
            # For now, let's just stick to AbstractClassNode behavior and ignore parsed stereotype
            # if it conflicts, or maybe log a warning?
            pass

        return AbstractClassNode(
            class_name=name,
            attributes=attributes,
            methods=methods,
            # stereotype=stereotype, # REMOVED to avoid TypeError
            **kwargs,
        )

    elif node_type == "enum":
        node_kwargs = kwargs.copy()
        if "spot" not in node_kwargs:
            node_kwargs["spot"] = "E"

        if not stereotype:
            stereotype = "enumeration"  # Changed from "enum" to "enumeration"

        return ClassNode(
            class_name=name,
            attributes=attributes,
            methods=methods,
            stereotype=stereotype,
            **node_kwargs,
        )

    else:  # Standard class
        return ClassNode(
            class_name=name,
            attributes=attributes,
            methods=methods,
            stereotype=stereotype,
            **kwargs,
        )
