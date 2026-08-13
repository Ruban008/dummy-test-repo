import pytest
from unittest.mock import MagicMock
from math_ops import add


@pytest.fixture
def mock_addable_object():
    """Provides a mock object that implements addition interface."""
    obj = MagicMock()
    obj.__add__ = MagicMock(return_value="mocked_sum")
    return obj


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # Standard Integer Addition
        (1, 2, 3),
        (-1, 1, 0),
        (-5, -5, -10),
        (0, 0, 0),
        
        # Large Integers
        (10**18, 10**18, 2 * 10**18),
        
        # Float Addition
        (1.5, 2.5, 4.0),
        (-1.1, 1.1, 0.0),
        
        # String Concatenation
        ("hello ", "world", "hello world"),
        ("", "", ""),
        
        # List Concatenation
        ([1, 2], [3, 4], [1, 2, 3, 4]),
        ([], [], []),
        
        # Tuple Concatenation
        ((1, 2), (3, 4), (1, 2, 3, 4)),
    ],
    ids=[
        "pos_integers", "pos_neg_integers", "neg_integers", "zeros",
        "large_integers", "floats", "cancelling_floats",
        "strings", "empty_strings",
        "lists", "empty_lists",
        "tuples"
    ]
)
def test_add_valid_inputs_returns_expected(a, b, expected):
    """Verify that add correctly computes the sum of compatible types."""
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected_approx",
    [
        (0.1, 0.2, 0.3),
        (0.1 + 0.1 + 0.1, 0.3, 0.3)
    ],
    ids=["floating_point_precision", "accumulated_float_precision"]
)
def test_add_float_precision_with_approx(a, b, expected_approx):
    """Verify float addition handling precision issues using pytest.approx."""
    assert add(a, b) == pytest.approx(expected_approx)


@pytest.mark.parametrize(
    "a, b",
    [
        (1, "2"),
        ("1", 2),
        ([1], (2,)),
        (None, 1),
        (1, None),
    ],
    ids=[
        "int_and_str", "str_and_int", "list_and_tuple", 
        "none_and_int", "int_and_none"
    ]
)
def test_add_incompatible_types_raises_type_error(a, b):
    """Verify that adding incompatible types raises a TypeError with appropriate messages."""
    with pytest.raises(TypeError) as exc_info:
        add(a, b)
    
    # Assert that the error message contains expected signature-related phrases
    err_msg = str(exc_info.value).lower()
    assert any(phrase in err_msg for phrase in ["unsupported operand type", "can only concatenate", "must be"])


def test_add_invokes_dunder_add_on_operand(mock_addable_object):
    """Verify that add successfully delegates to the __add__ magic method of the operand."""
    result = add(mock_addable_object, 5)
    
    mock_addable_object.__add__.assert_called_once_with(5)
    assert result == "mocked_sum"