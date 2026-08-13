import pytest
from unittest.mock import MagicMock
from math_ops import add


@pytest.fixture
def custom_addable_factory():
    """Fixture that provides a factory for custom objects with __add__ implemented."""
    class CustomAddable:
        def __init__(self, val):
            self.val = val

        def __add__(self, other):
            if isinstance(other, CustomAddable):
                return CustomAddable(self.val + other.val)
            return NotImplemented

        def __eq__(self, other):
            return isinstance(other, CustomAddable) and self.val == other.val

        def __repr__(self):
            return f"CustomAddable({self.val})"

    return CustomAddable


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (-1, -1, -2),
        (-1, 1, 0),
        (0, 0, 0),
        (10**18, 10**18, 2 * 10**18),
        (1.5, 2.5, 4.0),
        (-1.5, 1.5, 0.0),
        (0.1, 0.2, pytest.approx(0.3)),
        ("hello ", "world", "hello world"),
        ([1, 2], [3, 4], [1, 2, 3, 4]),
        ((1, 2), (3, 4), (1, 2, 3, 4)),
    ],
    ids=[
        "positive_integers",
        "negative_integers",
        "mixed_sign_integers",
        "zeros",
        "extremely_large_integers",
        "positive_floats",
        "mixed_sign_floats",
        "float_precision_approx",
        "string_concatenation",
        "list_concatenation",
        "tuple_concatenation",
    ]
)
def test_add_valid_inputs_returns_expected_result(a, b, expected):
    """Verify that add correctly computes sum or concatenation of valid matching types."""
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected_exception",
    [
        (1, "2", TypeError),
        ("1", 2, TypeError),
        ([1], 2, TypeError),
        (2, [1], TypeError),
        ("string", [1, 2], TypeError),
    ],
    ids=[
        "int_and_str",
        "str_and_int",
        "list_and_int",
        "int_and_list",
        "str_and_list",
    ]
)
def test_add_invalid_types_raises_type_error(a, b, expected_exception):
    """Verify that add raises TypeError when called with incompatible types."""
    with pytest.raises(expected_exception):
        add(a, b)


def test_add_custom_objects_returns_summed_object(custom_addable_factory):
    """Verify that add works correctly with custom user-defined types implementing __add__."""
    obj1 = custom_addable_factory(10)
    obj2 = custom_addable_factory(20)
    expected = custom_addable_factory(30)
    assert add(obj1, obj2) == expected


def test_add_delegates_to_magic_add_method():
    """Verify that the add function delegates operation execution to the __add__ magic method."""
    mock_a = MagicMock()
    mock_b = MagicMock()

    _ = add(mock_a, mock_b)

    mock_a.__add__.assert_called_once_with(mock_b)