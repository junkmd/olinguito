from typing import Annotated, Literal, TypedDict

import pytest

import olinguito
from olinguito.generating import generate_json_schema


class Test_generate_json_schema:
    def test_int_argument(self):
        def func(a: int): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "integer"}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_str_argument(self):
        def func(a: str): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "string"}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_bool_argument(self):
        def func(a: bool): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "boolean"}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_none_argument(self):
        def func(a: int | None): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": ["integer", "null"]}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_union_argument(self):
        def func(a: int | str): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": ["integer", "string"]}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_annotated_argument(self):
        def func(a: Annotated[int, olinguito.description("This is an integer")]): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "This is an integer"}
            },
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_int_literals(self):
        def func(a: Literal[1, 2]): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "integer", "enum": [1, 2]}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_str_literals(self):
        def func(a: Literal["foo", "bar"]): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "string", "enum": ["foo", "bar"]}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_bool_literals(self):
        def func(a: Literal[True]): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "boolean", "enum": [True]}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_mixed_literals(self):
        def func(a: Literal["foo", 1, False]): ...

        with pytest.raises(TypeError):
            generate_json_schema(func)

    def test_multiple_arguments(self):
        def func(a: int, b: str): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "string"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        }

    def test_multiple_arguments_with_optional(self):
        def func(a: int, b: str | None): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": ["string", "null"]}},
            "required": ["a", "b"],
            "additionalProperties": False,
        }

    def test_multiple_arguments_with_union(self):
        def func(a: int | str, b: bool | None): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {
                "a": {"type": ["integer", "string"]},
                "b": {"type": ["boolean", "null"]},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        }

    def test_multiple_arguments_with_annotated(self):
        def func(a: int, b: str): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "string"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        }

    def test_list_argument(self):
        def func(a: list[int]): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {"a": {"type": "array", "items": {"type": "integer"}}},
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_typed_dict_argument(self):
        class _D(TypedDict):
            foo: str
            bar: int

        def func(a: _D): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {
                "a": {
                    "type": "object",
                    "properties": {
                        "foo": {"type": "string"},
                        "bar": {"type": "integer"},
                    },
                    "required": ["foo", "bar"],
                    "additionalProperties": False,
                }
            },
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_list_and_typed_dict_argument(self):
        class _D(TypedDict):
            foo: str
            bar: int

        def func(a: list[_D]): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {
                "a": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "foo": {"type": "string"},
                            "bar": {"type": "integer"},
                        },
                        "required": ["foo", "bar"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_optional_typed_dict_argument(self):
        class _D(TypedDict):
            foo: str
            bar: int

        def func(a: _D | None): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {
                "a": {
                    "type": ["object", "null"],
                    "properties": {
                        "foo": {"type": "string"},
                        "bar": {"type": "integer"},
                    },
                    "required": ["foo", "bar"],
                    "additionalProperties": False,
                }
            },
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_union_with_list_and_typed_dict(self):
        class _D(TypedDict):
            foo: str
            bar: int

        def func(a: list[_D] | str): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {
                "a": {
                    "type": ["array", "string"],
                    "items": {
                        "type": "object",
                        "properties": {
                            "foo": {"type": "string"},
                            "bar": {"type": "integer"},
                        },
                        "required": ["foo", "bar"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["a"],
            "additionalProperties": False,
        }

    def test_no_arguments(self):
        def func(): ...

        assert generate_json_schema(func) == {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        }
