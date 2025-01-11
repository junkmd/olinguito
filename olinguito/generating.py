import inspect
from collections.abc import Callable
from typing import Any, Literal, TypedDict

from .schema import _SchemaType, to_schema_type


class JsonSchema(TypedDict):
    type: Literal["object"]
    properties: dict[str, _SchemaType]
    required: list[str]
    additionalProperties: Literal[False]


def generate_json_schema(func: Callable[..., Any]) -> JsonSchema:
    signature = inspect.signature(func)
    properties: dict[str, _SchemaType] = {}
    required: list[str] = []
    for name, param in signature.parameters.items():
        properties[name] = to_schema_type(param.annotation)
        required.append(name)
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }
