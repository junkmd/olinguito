import types
import typing
import warnings
from dataclasses import dataclass
from typing import Any, List, Literal, NotRequired, TypedDict

from . import typeguards


class _DescriptionDict(TypedDict):
    description: str


@dataclass(frozen=True)
class _Mark:
    content: _DescriptionDict


def description(text: str) -> _Mark:
    return _Mark({"description": text})


class _SchemaType(TypedDict):
    type: str | list[str]
    items: NotRequired["_SchemaType"]
    description: NotRequired[str]
    properties: NotRequired[dict[str, "_SchemaType"]]
    required: NotRequired[list[str]]
    additionalProperties: NotRequired[Literal[False]]


def to_schema_type(anno: Any, /) -> _SchemaType:
    if anno is int:
        return {"type": "integer"}
    elif anno is float:
        return {"type": "number"}
    elif anno is str:
        return {"type": "string"}
    elif anno is bool:
        return {"type": "boolean"}
    elif typing.get_origin(anno) in (list, List):
        return {"type": "array", "items": to_schema_type(typing.get_args(anno)[0])}
    elif anno is types.NoneType:
        return {"type": "null"}
    elif typeguards.is_union(anno):
        return _to_union_schema_type(anno)
    elif typeguards.is_typeddict(anno):
        return _to_typeddict_schema_type(anno)
    elif typeguards.is_annotated(anno):
        return _to_annotated_schema_type(anno)
    raise TypeError  # pragma: no cover


def _to_union_schema_type(anno: typeguards.UnionOrAlias) -> _SchemaType:
    arguments: list[str] = []
    schemas: list[_SchemaType] = []
    for arg in typing.get_args(anno):
        schema = to_schema_type(arg)
        typ = schema["type"]
        if isinstance(typ, list):
            warnings.warn(f"Unexpected symbol: {typ}", UserWarning)  # pragma: no cover
        else:
            arguments.append(typ)
        if "properties" in schema or "items" in schema:
            schemas.append(schema)
    result: _SchemaType = {"type": arguments}
    for schema in schemas:
        if "properties" in schema:
            result["properties"] = schema["properties"]
        if "required" in schema:
            result["required"] = schema["required"]
        if "additionalProperties" in schema:
            result["additionalProperties"] = schema["additionalProperties"]
        if "items" in schema:
            result["items"] = schema["items"]
    return result


def _to_typeddict_schema_type(anno: typeguards.SubTypedDict) -> _SchemaType:
    properties = {}
    required = []
    for field, field_type in typing.get_type_hints(anno).items():
        properties[field] = to_schema_type(field_type)
        required.append(field)
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def _to_annotated_schema_type(anno: typeguards.AnnoAlias) -> _SchemaType:
    origin = anno.__origin__
    marks = [m for m in anno.__metadata__ if isinstance(m, _Mark)]
    if len(marks) > 1:
        raise ValueError  # pragma: no cover
    elif len(marks) == 1:
        return {**marks[0].content, **to_schema_type(origin)}
    else:
        return to_schema_type(origin)
