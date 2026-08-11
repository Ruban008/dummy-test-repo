import pytest
from math_ops import add

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (-5, -5, -10),
    (0, 0, 0),
    (1.5, 2.5, 4.0),
    (-1.5, 1.5, 0.0),
    (10**18, 10**18, 2 * 10**18),
    ("hello ", "world", "hello world"),
    ([1, 2], [3, 4], [1, 2, 3, 4]),
    ((1, 2), (3, 4), (1, 2, 3, 4)),
])
def test_add_supported_types(a, b, expected):
    assert add(a, b) == expected

def test_add_type_mismatch_raises_error():
    with pytest.raises(TypeError):
        add(1, "2")

    with pytest.raises(TypeError):
        add("1", 2)

    with pytest.raises(TypeError):
        add([1], (2,))

def test_add_missing_arguments():
    with pytest.raises(TypeError):
        add(1)

    with pytest.raises(TypeError):
        add()