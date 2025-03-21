import olinguito


@olinguito.wrap
def add(x: int, y: int) -> int:
    """Adds two integers."""
    return x + y


@olinguito.wrap
def multiply(x: int, y: int) -> int:
    """Multiplies two integers."""
    return x * y


@olinguito.wrap
def greet(name: str) -> str:
    """Returns a greeting message."""
    return f"Hello, {name}!"


class Test_Mapping:
    def test_dunder_getitem(self):
        mapping = olinguito.Mapping(add, multiply, greet)
        assert mapping["add"] is add
        assert mapping["multiply"] is multiply
        assert mapping["greet"] is greet

    def test_dunder_iter(self):
        mapping = olinguito.Mapping(add, multiply)
        add_, multiply_ = mapping
        assert add_ is add
        assert multiply_ is multiply

    def test_dunder_bool(self):
        assert not olinguito.Mapping()
        assert olinguito.Mapping(add)

    def test_dunder_contains(self):
        mapping = olinguito.Mapping(add, multiply)
        assert "add" in mapping
        assert "multiply" in mapping
        assert "greet" not in mapping
        assert add in mapping
        assert multiply in mapping
        assert greet not in mapping

    def test_dunder_len(self):
        assert len(olinguito.Mapping()) == 0
        assert len(olinguito.Mapping(add)) == 1
        assert len(olinguito.Mapping(add, multiply)) == 2

    def test_dunder_call(self):
        mapping = olinguito.Mapping(add, multiply, greet)
        assert mapping("add", 3, 4) == 7
        assert mapping("multiply", 3, 4) == 12
        assert mapping("greet", name="Alice") == "Hello, Alice!"
