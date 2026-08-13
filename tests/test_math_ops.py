import math
from unittest.mock import MagicMock
import pytest
from math_ops import add


class CustomNumber:
    """A custom class implementing __add__ to verify compatibility with custom objects."""

    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: "CustomNumber") -> "CustomNumber":
        if isinstance(other, CustomNumber):
            return CustomNumber(self.value + other.value)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomNumber):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        return f"CustomNumber({self.value})"


@pytest.fixture
def custom_number_operands():
    """Provides a pair of CustomNumber instances and their expected sum."""
    operand_a = CustomNumber(10)
    operand_b = CustomNumber(20)
    expected_sum = CustomNumber(30)
    return operand_a, operand_b, expected_sum


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # Integer boundary conditions & basic math
        (0, 0, 0),
        (1, 2, 3),
        (-1, 1, 0),
        (-5, -5, -10),
        (999999999999999999, 1, 1000000000000000000),
        # Float arithmetic & IEEE 754 precision representation
        (1.5, 2.5, 4.0),
        (-1.5, 1.5, 0.0),
        (-0.0, 0.0, 0.0),
        (0.1, 0.2, 0.3),  # Note: assert using pytest.approx for precision safety in tests
        # Mixed scalar types
        (1, 2.5, 3.5),
        (-1, 1.0, 0.0),
        # String concatenation
        ("hello ", "world", "hello world"),
        ("", "empty_start", "empty_start"),
        # List sequence combination
        ([1, 2], [3, 4], [1, 2, 3, 4]),
        ([], [1], [1]),
        # Tuple sequence combination
        ((1, 2), (3, 4), (1, 2, 3, 4)),
    ],
    ids=[
        "zero_identity",
        "positive_integers",
        "negative_and_positive_integer",
        "negative_integers",
        "large_integers_boundary",
        "positive_floats",
        "negative_and_positive_floats",
        "signed_zeros",
        "floating_point_precision",
        "mixed_int_float",
        "mixed_negative_int_float",
        "string_concatenation",
        "empty_string_concatenation",
        "list_concatenation",
        "empty_list_concatenation",
        "tuple_concatenation",
    ]
)
def test_add_success_cases(a, b, expected):
    """Verify that add successfully calculates sums for standard equivalence classes."""
    if isinstance(expected, float):
        assert add(a, b) == pytest.approx(expected)
    else:
        assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected_fn",
    [
        (float("inf"), 1.0, lambda res: math.isinf(res) and res > 0),
        (float("-inf"), 1.0, lambda res: math.isinf(res) and res < 0),
        (float("inf"), float("-inf"), lambda res: math.isnan(res)),
        (float("nan"), 5.0, lambda res: math.isnan(res)),
    ],
    ids=[
        "positive_infinity",
        "negative_infinity",
        "infinity_cancellation",
        "nan_operand"
    ]
)
def test_add_float_extreme_cases(a, b, expected_fn):
    """Verify standard IEEE-754 behaviors for special floating-point edge cases."""
    result = add(a, b)
    assert expected_fn(result)


def test_add_custom_objects(custom_number_operands):
    """Verify that the add function respects polymorphic type protocol interfaces."""
    op_a, op_b, expected = custom_number_operands
    assert add(op_a, op_b) == expected


@pytest.mark.parametrize(
    "a, b, expected_error",
    [
        (1, "2", TypeError),
        ("1", 2, TypeError),
        ([1], (2,), TypeError),
        (None, 5, TypeError),
        (5, None, TypeError),
    ],
    ids=[
        "int_and_str",
        "str_and_int",
        "list_and_tuple",
        "none_and_int",
        "int_and_none"
    ]
)
def test_add_type_exceptions(a, b, expected_error):
    """Verify that attempting to add incompatible classes raises TypeError."""
    with pytest.raises(expected_error) as exc_info:
        add(a, b)
    assert "unsupported operand type" in str(exc_info.value) or "can only concatenate" in str(exc_info.value)


def test_add_delegates_to_operand_magic_method():
    """Verify internal integration behavior using mocks to isolate execution path.

    Ensures that the add function depends directly on delegation to __add__.
    """
    mock_a = MagicMock()
    mock_b = MagicMock()
    
    # Configure mock return value for __add__ protocol execution
    mock_a.__add__.return_value = "mock_sum_value"
    
    result = add(mock_a, mock_b)
    
    # Validate interaction isolation boundaries
    mock_a.__add__.assert_called_once_with(mock_b)
    assert result == "mock_sum_value"