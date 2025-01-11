import functools
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, ParamSpec, TypeVar

from .generating import JsonSchema, generate_json_schema

_P = ParamSpec("_P")
_R = TypeVar("_R")


@dataclass
class Wrapper(Generic[_P, _R]):
    """A callable wrapper class with JSON schema metadata for its signature
    and documentation.
    """

    func: Callable[_P, _R]
    """The wrapped function."""
    parameters: JsonSchema
    """The JSON schema representation of the function's signature."""
    doc: str
    """The docstring of the wrapped function."""

    @property
    def name(self) -> str:
        """Retrieves the name of the wrapped function."""
        return self.func.__name__

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        return self.func(*args, **kwargs)


def wrap(func: Callable[_P, _R]) -> Wrapper[_P, _R]:
    """Wraps a function, attaching JSON schema metadata for its signature and
    retaining its documentation.

    Args:
        func (Callable[..., Any]): The function to be wrapped.

    Returns:
        Wrapper[..., Any]: A Wrapper instance.

    Raises:
        TypeError: If the function does not have a docstring.
    """
    doc = func.__doc__
    if doc is None:
        raise TypeError
    w = Wrapper(func, generate_json_schema(func), doc)
    functools.update_wrapper(w, func)
    return w
