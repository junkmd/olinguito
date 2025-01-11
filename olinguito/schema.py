import types
import typing
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
    raise TypeError


def _to_union_schema_type(anno: typeguards.UnionOrAlias) -> _SchemaType:
    arguments: list[str] = []
    for arg in typing.get_args(anno):
        typ = to_schema_type(arg)["type"]
        if isinstance(typ, list):
            arguments.extend(typ)
        else:
            arguments.append(typ)
    return {"type": arguments}


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
        raise ValueError
    elif len(marks) == 1:
        return {**marks[0].content, **to_schema_type(origin)}
    else:
        return to_schema_type(origin)
