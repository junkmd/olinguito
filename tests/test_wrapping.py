from typing import Annotated

import pytest

import olinguito


class Test_wrap:
    def test_wrap_single_argument(self):
        @olinguito.wrap
        def func(a: Annotated[int, olinguito.description("param")]) -> str:
            """This is a simple function."""
            return str(a)

        assert func(123) == "123"
        assert func.parameters == {
            "type": "object",
            "properties": {"a": {"type": "integer", "description": "param"}},
            "required": ["a"],
            "additionalProperties": False,
        }
        assert func.doc == "This is a simple function."
        assert func.name == "func"

    def test_wrap_multiple_arguments(self):
        @olinguito.wrap
        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b

        assert add(3, 4) == 7
        assert add.parameters == {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        }
        assert add.doc == "Add two numbers."
        assert add.name == "add"

    def test_wrap_no_docstring(self):
        def no_doc_func(a: int) -> str:
            return str(a)

        with pytest.raises(TypeError):
            olinguito.wrap(no_doc_func)

    def test_wrap_with_complex_type(self):
        @olinguito.wrap
        def func(a: int, b: str) -> bool:
            """Check if a is greater than the length of b."""
            return a > len(b)

        assert func(5, "test") is True
        assert func.parameters == {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "string"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        }
        assert func.doc == "Check if a is greater than the length of b."
        assert func.name == "func"
