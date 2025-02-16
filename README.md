# olinguito

![Python](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)  [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

`olinguito` is a lightweight Python library that provides a simple way to generate JSON schemas based on function signatures.  
It wraps functions and automatically creates JSON schemas that describe their parameters.  
This is particularly useful for validating input arguments in APIs or other dynamic environments.


## Features

- Generate JSON schemas based on function signatures.
- Supports Python's type hints, including:
  - Primitive types ([`int`](https://docs.python.org/3/library/functions.html#int), [`str`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [`bool`](https://docs.python.org/3/library/stdtypes.html#typebool), etc.)
  - [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict) for complex objects
  - [`Union`](https://docs.python.org/3/library/typing.html#typing.Union), [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional), and [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated)
  - Nested [`list`](https://docs.python.org/3/library/stdtypes.html#list)s and objects
- Provides a convenient `wrap` function to decorate and manage schema-aware functions.


## Usage

Here are some example use cases:


### Wrapping a Simple Function

```py
>>> import pprint
>>> import olinguito
>>> @olinguito.wrap
... def add(a: int, b: int) -> int:
...     """Adds two integers."""
...     return a + b
...
>>> add.func  # doctest: +ELLIPSIS
<function add at ...>
>>> pprint.pprint(add.parameters)
{'additionalProperties': False,
 'properties': {'a': {'type': 'integer'}, 'b': {'type': 'integer'}},
 'required': ['a', 'b'],
 'type': 'object'}
>>> add.doc
'Adds two integers.'
>>> add.name
'add'
>>> add(1, 2)
3
>>>
```

### Working with `TypedDict`

```py
>>> from typing import TypedDict
>>> class User(TypedDict):
...     name: str
...     age: int | None
...
>>> @olinguito.wrap
... def create_user(user: User) -> str:
...     """Creates a user and returns a confirmation message."""
...     return f"User {user['name']} created."
...
>>> create_user.func  # doctest: +ELLIPSIS
<function create_user at ...>
>>> pprint.pprint(create_user.parameters)
{'additionalProperties': False,
 'properties': {'user': {'additionalProperties': False,
                         'properties': {'age': {'type': ['integer', 'null']},
                                        'name': {'type': 'string'}},
                         'required': ['name', 'age'],
                         'type': 'object'}},
 'required': ['user'],
 'type': 'object'}
>>> create_user.doc
'Creates a user and returns a confirmation message.'
>>> create_user.name
'create_user'
>>> create_user({'name': 'Graham'})
'User Graham created.'
>>>
```

### Using `Annotated` for Descriptions

```py
>>> from typing import Annotated
>>> @olinguito.wrap
... def process_item(
...     item_id: Annotated[int, olinguito.description("The ID of the item")],
...     quantity: Annotated[int, olinguito.description("Quantity to process")]
... ) -> bool:
...     """Processes an item."""
...     return quantity > 0
...
>>> process_item.func  # doctest: +ELLIPSIS
<function process_item at ...>
>>> pprint.pprint(process_item.parameters)
{'additionalProperties': False,
 'properties': {'item_id': {'description': 'The ID of the item',
                            'type': 'integer'},
                'quantity': {'description': 'Quantity to process',
                             'type': 'integer'}},
 'required': ['item_id', 'quantity'],
 'type': 'object'}
>>> process_item.doc
'Processes an item.'
>>> process_item.name
'process_item'
>>> process_item(3, 2)
True
>>>
```

### `Mapping` Utilities

```py
>>> @olinguito.wrap
... def subtract(x: int, y: int) -> int:
...     """Subtracts two integers."""
...     return x - y
...
>>> @olinguito.wrap
... def multiply(x: int, y: int) -> int:
...     """Multiplies two integers."""
...     return x * y
...
>>> mapping = olinguito.Mapping(add, multiply)
>>> len(mapping)
2
>>> mapping["multiply"](2, 3)  # Accessing via item lookup
6
>>> mapping("subtract", 6, 5)  # Calling functions by name
1
>>>
```

## Why "olinguito"?

The [**olinguito**](https://en.wikipedia.org/wiki/Olinguito) is a small, agile mammal found in the cloud forests of the Andes.  
Similarly, this library is designed to be lightweight, focused, and straightforward for your Python projects.


## License

This project is licensed under the MIT License.


## Contributions

Contributions are welcome!  
Please feel free to open an issue or submit a pull request.
