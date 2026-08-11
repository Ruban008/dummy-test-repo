import pytest
from math_ops import add

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (-5, -5, -10),
    (0, 0, 0),
    (1000000, 2000000, 3000000),
])
def test_add_integers(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (1.5, 2.5, 4.0),
    (-1.1, 1.1, 0.0),
    (0.1, 0.2, 0.3),
])
def test_add_floats(a, b, expected):
    assert add(a, b) == pytest.approx(expected)

def test_add_strings():
    assert add("hello ", "world") == "hello world"

def test_add_lists():
    assert add([1, 2], [3, 4]) == [1, 2, 3, 4]

def test_add_incompatible_types_raises_error():
    with pytest.raises(TypeError):
        add(1, "2")

    with pytest.raises(TypeError):
        add([1], 2)