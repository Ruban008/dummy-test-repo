"""Tests for the public behavior of math_ops.add."""

import unittest

from math_ops import add


class TestAdd(unittest.TestCase):
    def test_adds_positive_integers(self):
        self.assertEqual(add(2, 3), 5)

    def test_zero_is_an_identity_on_either_side(self):
        for value in (0, 1, -7, 4.5):
            with self.subTest(value=value):
                self.assertEqual(add(value, 0), value)
                self.assertEqual(add(0, value), value)

    def test_adds_negative_and_mixed_sign_integers(self):
        self.assertEqual(add(-4, -6), -10)
        self.assertEqual(add(-4, 6), 2)
        self.assertEqual(add(4, -6), -2)

    def test_adds_floating_point_numbers(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)
        self.assertAlmostEqual(add(-1.25, 3.5), 2.25)

    def test_adds_large_integers_without_losing_precision(self):
        left = 10**100
        right = 10**80
        self.assertEqual(add(left, right), left + right)

    def test_addition_is_commutative_for_numeric_inputs(self):
        examples = ((2, 9), (-3, 8), (2.5, 0.75), (0, -12))
        for left, right in examples:
            with self.subTest(left=left, right=right):
                self.assertEqual(add(left, right), add(right, left))

    def test_incompatible_operand_types_raise_type_error(self):
        examples = ((1, "2"), ("1", 2), (None, 1), (1, None))
        for left, right in examples:
            with self.subTest(left=left, right=right):
                with self.assertRaises(TypeError):
                    add(left, right)

    def test_wrong_number_of_arguments_raises_type_error(self):
        with self.assertRaises(TypeError):
            add(1)
        with self.assertRaises(TypeError):
            add(1, 2, 3)


if __name__ == "__main__":
    unittest.main()
