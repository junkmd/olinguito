import inspect
import typing
from types import UnionType
from typing import Annotated, Any, Protocol, TypeGuard, Union


class AnnoAlias(Protocol):
    __origin__: str | type[Any]
    __metadata__: tuple[Any, ...]


def is_annotated(obj: Any) -> TypeGuard[AnnoAlias]:
    return typing.get_origin(obj) is Annotated


class UnionOrAlias(Protocol):
    __origin__: tuple[type[Any], ...]


def is_union(obj: Any) -> TypeGuard[UnionOrAlias]:
    return typing.get_origin(obj) in (UnionType, Union)


class SubTypedDict(Protocol):
    __annotations__: dict[str, Any]


def is_typeddict(obj: Any) -> TypeGuard[SubTypedDict]:
    return (
        inspect.isclass(obj)
        and issubclass(obj, dict)
        and hasattr(obj, "__annotations__")
    )
