import collections.abc
import types
from dataclasses import dataclass
from typing import Any

from .wrapping import Wrapper


@dataclass(init=False, frozen=True, repr=False)
class Mapping:
    data: collections.abc.Mapping[str, Wrapper[..., Any]]

    def __init__(self, *wrappers: Wrapper[..., Any]) -> None:
        object.__setattr__(
            self, "data", types.MappingProxyType({w.name: w for w in wrappers})
        )

    def __getitem__(self, key: str) -> Wrapper[..., Any]:
        return self.data[key]

    def __iter__(self) -> collections.abc.Iterator[Wrapper[..., Any]]:
        yield from self.data.values()

    def __bool__(self) -> bool:
        return bool(self.data)

    def __contains__(self, key: Any) -> bool:
        if isinstance(key, str):
            return key in self.data
        return key in tuple(self.data.values())

    def __len__(self) -> int:
        return len(self.data)

    def __call__(self, key: str, *args: Any, **kwargs: Any) -> Any:
        return self.data[key](*args, **kwargs)
