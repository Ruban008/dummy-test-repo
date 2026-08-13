import pytest
from unittest.mock import MagicMock
from math_ops import add


class CustomNumeric:
    """A custom class implementing __add__ to test polymorphism."""

    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: "CustomNumeric") -> "CustomNumeric":
        if not isinstance(other, CustomNumeric):
            return NotImplemented
        return CustomNumeric(self.value + other.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomNumeric):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        return f"CustomNumeric({self.value})"


@pytest.fixture
def custom_numeric_factory():
    """Fixture providing a factory for CustomNumeric instances."""
    def _make_custom(value: int) -> CustomNumeric:
        return CustomNumeric(value)
    return _make_custom


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # Standard integer addition
        (1, 2, 3),
        (-1, 1, 0),
        (-5, -5, -10),
        (0, 0, 0),
        # Large integers (arbitrary precision in Python)
        (10**18, 10**18, 2 * 10**18),
        # Floating point addition
        (1.5, 2.5, 4.0),
        (-1.1, 1.1, 0.0),
        (0.0, -0.0, 0.0),
        # Mixed numeric types (float and int)
        (1, 2.5, 3.5),
        (2.5, 1, 3.5),
        # Sequence concatenation (duck typing validation)
        ("hello ", "world", "hello world"),
        ([1, 2], [3, 4], [1, 2, 3, 4]),
        ((1, 2), (3, 4), (1, 2, 3, 4)),
    ],
    ids=[
        "positive_integers",
        "mixed_sign_integers",
        "negative_integers",
        "zeros",
        "large_integers",
        "positive_floats",
        "mixed_sign_floats",
        "signed_zeros",
        "int_and_float",
        "float_and_int",
        "strings",
        "lists",
        "tuples",
    ]
)
def test_add_valid_inputs_returns_expected_result(a, b, expected):
    """Verify that add() correctly evaluates standard numeric and sequence types."""
    assert add(a, b) == expected


def test_add_custom_objects_defines_polymorphism(custom_numeric_factory):
    """Verify that add() works seamlessly with custom user-defined classes implementing __add__."""
    obj1 = custom_numeric_factory(10)
    obj2 = custom_numeric_factory(20)
    expected = custom_numeric_factory(30)

    result = add(obj1, obj2)

    assert result == expected
    assert isinstance(result, CustomNumeric)


def test_add_invokes_dunder_add_on_operand():
    """Verify that add() delegates execution to the operand's __add__ method using MagicMock."""
    mock_operand_a = MagicMock()
    mock_operand_b = MagicMock()

    add(mock_operand_a, mock_operand_b)

    mock_operand_a.__add__.assert_called_once_with(mock_operand_b)


@pytest.mark.parametrize(
    "a, b, expected_exception, match_pattern",
    [
        (1, "string", TypeError, "unsupported operand type"),
        ("string", 1, TypeError, "can only concatenate str"),
        ([1, 2], (3, 4), TypeError, "can only concatenate list"),
        (None, 5, TypeError, "unsupported operand type"),
    ],
    ids=[
        "int_and_str",
        "str_and_int",
        "list_and_tuple",
        "none_and_int",
    ]
)
def test_add_incompatible_types_raises_type_error(a, b, expected_exception, match_pattern):
    """Verify that add() raises a TypeError with appropriate message when operands are incompatible."""
    with pytest.raises(expected_exception, match=match_pattern):
        add(a, b)