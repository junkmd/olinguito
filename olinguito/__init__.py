"""A Python function decorator generating JSON schema based on signatures."""

__version__ = "0.1.0"

from .mapping import Mapping  # noqa
from .schema import description  # noqa
from .wrapping import Wrapper, wrap  # noqa
