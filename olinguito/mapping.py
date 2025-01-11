import collections.abc
from dataclasses import dataclass
from typing import Any

from .wrapping import Wrapper


@dataclass(init=False, frozen=True)
class Mapping:
    data: collections.abc.Mapping[str, Wrapper[..., Any]]

    def __init__(self, *wrappers: Wrapper[..., Any]) -> None:
        object.__setattr__(self, "data", {w.name: w for w in wrappers})

    def __getitem__(self, key: str) -> Wrapper[..., Any]:
        return self.data[key]

    def __iter__(self) -> collections.abc.Iterator[Wrapper[..., Any]]:
        yield from self.data.values()

    def __call__(self, key: str, *args: Any, **kwargs: Any) -> Any:
        return self.data[key](*args, **kwargs)
