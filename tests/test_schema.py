import types
from typing import Annotated, Optional, TypedDict, Union

import olinguito
from olinguito.schema import to_schema_type


class Test_to_schema_type:
    def test_int(self):
        assert to_schema_type(int) == {"type": "integer"}

    def test_float(self):
        assert to_schema_type(float) == {"type": "number"}

    def test_str(self):
        assert to_schema_type(str) == {"type": "string"}

    def test_bool(self):
        assert to_schema_type(bool) == {"type": "boolean"}

    def test_none(self):
        assert to_schema_type(types.NoneType) == {"type": "null"}

    def test_list(self):
        assert to_schema_type(list[str]) == {
            "type": "array",
            "items": {"type": "string"},
        }

    def test_typeddict(self):
        class _D(TypedDict):
            foo: str
            bar: int | None

        assert to_schema_type(_D) == {
            "type": "object",
            "properties": {
                "foo": {"type": "string"},
                "bar": {"type": ["integer", "null"]},
            },
            "required": ["foo", "bar"],
            "additionalProperties": False,
        }

    def test_annotated(self):
        assert to_schema_type(Annotated[int, olinguito.description("foo"), "bar"]) == {
            "type": "integer",
            "description": "foo",
        }
        assert to_schema_type(Annotated[int, "bar"]) == {"type": "integer"}

    def test_union(self):
        assert to_schema_type(int | str) == {"type": ["integer", "string"]}
        assert to_schema_type(Union[int, str]) == {"type": ["integer", "string"]}
        assert to_schema_type(int | None) == {"type": ["integer", "null"]}
        assert to_schema_type(Optional[int]) == {"type": ["integer", "null"]}
        assert to_schema_type(int | str | None) == {
            "type": ["integer", "string", "null"]
        }
        assert to_schema_type(Union[int | str, None]) == {
            "type": ["integer", "string", "null"]
        }
        assert to_schema_type(Union[int | Union[str, float, None]]) == {
            "type": ["integer", "string", "number", "null"]
        }

    def test_optional_typeddict(self):
        class _D(TypedDict):
            foo: str
            bar: int | None

        assert to_schema_type(_D | None) == {
            "type": ["object", "null"],
            "properties": {
                "foo": {"type": "string"},
                "bar": {"type": ["integer", "null"]},
            },
            "required": ["foo", "bar"],
            "additionalProperties": False,
        }

    def test_optional_list(self):
        assert to_schema_type(list[str] | None) == {
            "type": ["array", "null"],
            "items": {"type": "string"},
        }
