"""
Comprehensive test suite for matrix_operations module.

Tests cover:
- All basic operations (add, subtract, multiply, transpose)
- Determinant calculation
- Matrix inversion
- Scalar operations
- Error cases (dimension mismatches, singular matrices, non-square)
- Edge cases (empty, 1x1, 1xn, nx1, zero matrices)
- Numerical precision
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from matrix_operations import (
    Matrix,
    parse_matrix_string,
    matrix_add,
    matrix_subtract,
    matrix_multiply,
    matrix_transpose,
    matrix_determinant,
    matrix_inverse,
    scalar_multiply,
)


class TestMatrixInitialization(unittest.TestCase):
    """Test matrix initialization and validation."""

    def test_empty_matrix(self):
        """Test creation of empty matrix."""
        m = Matrix([[]])
        self.assertEqual(m.rows, 1)
        self.assertEqual(m.cols, 0)

    def test_single_element(self):
        """Test 1x1 matrix."""
        m = Matrix([[5]])
        self.assertEqual(m.rows, 1)
        self.assertEqual(m.cols, 1)
        self.assertEqual(m.data[0][0], 5)

    def test_rectangular_matrix(self):
        """Test rectangular matrix."""
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 3)

    def test_inconsistent_rows(self):
        """Test that inconsistent row lengths raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            Matrix([[1, 2], [3, 4, 5]])
        self.assertIn("Row 1", str(ctx.exception))

    def test_not_list_of_lists(self):
        """Test that non-list input raises TypeError."""
        with self.assertRaises(TypeError):
            Matrix([1, 2, 3])
        with self.assertRaises(TypeError):
            Matrix("not a list")

    def test_deep_copy(self):
        """Test that copy creates independent copy."""
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = m1.copy()
        m2.data[0][0] = 999
        self.assertNotEqual(m1.data[0][0], m2.data[0][0])


class TestMatrixAddition(unittest.TestCase):
    """Test matrix addition."""

    def test_add_simple(self):
        """Test simple 2x2 addition."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        result = A + B
        expected = Matrix([[6, 8], [10, 12]])
        self.assertEqual(result, expected)

    def test_add_rectangular(self):
        """Test addition of rectangular matrices."""
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        B = Matrix([[7, 8, 9], [10, 11, 12]])
        result = A + B
        expected = Matrix([[8, 10, 12], [14, 16, 18]])
        self.assertEqual(result, expected)

    def test_add_1x1(self):
        """Test addition of 1x1 matrices."""
        A = Matrix([[3]])
        B = Matrix([[5]])
        result = A + B
        self.assertEqual(result.data[0][0], 8)

    def test_add_column_vector(self):
        """Test addition of column vectors (nx1)."""
        A = Matrix([[1], [2], [3]])
        B = Matrix([[4], [5], [6]])
        result = A + B
        expected = Matrix([[5], [7], [9]])
        self.assertEqual(result, expected)

    def test_add_row_vector(self):
        """Test addition of row vectors (1xn)."""
        A = Matrix([[1, 2, 3]])
        B = Matrix([[4, 5, 6]])
        result = A + B
        expected = Matrix([[5, 7, 9]])
        self.assertEqual(result, expected)

    def test_add_dimension_mismatch(self):
        """Test that dimension mismatch raises ValueError."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError) as ctx:
            A + B
        self.assertIn("Dimension mismatch", str(ctx.exception))

    def test_add_non_matrix(self):
        """Test that adding non-Matrix raises TypeError."""
        A = Matrix([[1, 2], [3, 4]])
        with self.assertRaises(TypeError):
            A + 5

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        A = Matrix([[-1, -2], [-3, -4]])
        B = Matrix([[5, 6], [7, 8]])
        result = A + B
        expected = Matrix([[4, 4], [4, 4]])
        self.assertEqual(result, expected)


class TestMatrixSubtraction(unittest.TestCase):
    """Test matrix subtraction."""

    def test_subtract_simple(self):
        """Test simple 2x2 subtraction."""
        A = Matrix([[5, 6], [7, 8]])
        B = Matrix([[1, 2], [3, 4]])
        result = A - B
        expected = Matrix([[4, 4], [4, 4]])
        self.assertEqual(result, expected)

    def test_subtract_negative_result(self):
        """Test subtraction yielding negative result."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        result = A - B
        expected = Matrix([[-4, -4], [-4, -4]])
        self.assertEqual(result, expected)

    def test_subtract_dimension_mismatch(self):
        """Test that dimension mismatch raises ValueError."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3]])
        with self.assertRaises(ValueError):
            A - B

    def test_subtract_self(self):
        """Test subtracting matrix from itself yields zero."""
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        result = A - A
        expected = Matrix([[0, 0, 0], [0, 0, 0]])
        self.assertEqual(result, expected)


class TestMatrixMultiplication(unittest.TestCase):
    """Test matrix multiplication."""

    def test_multiply_2x2(self):
        """Test 2x2 matrix multiplication."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        result = A * B
        expected = Matrix([[19, 22], [43, 50]])
        self.assertEqual(result, expected)

    def test_multiply_non_square(self):
        """Test multiplication of non-square matrices."""
        A = Matrix([[1, 2, 3], [4, 5, 6]])  # 2x3
        B = Matrix([[7, 8], [9, 10], [11, 12]])  # 3x2
        result = A * B
        expected = Matrix([[58, 64], [139, 154]])
        self.assertEqual(result, expected)

    def test_multiply_identity(self):
        """Test multiplication with identity matrix."""
        A = Matrix([[1, 2], [3, 4]])
        I = Matrix([[1, 0], [0, 1]])
        result = A * I
        self.assertEqual(result, A)
        result2 = I * A
        self.assertEqual(result2, A)

    def test_multiply_dimension_mismatch(self):
        """Test that dimension mismatch raises ValueError."""
        A = Matrix([[1, 2], [3, 4]])  # 2x2
        B = Matrix([[1, 2, 3]])  # 1x3
        with self.assertRaises(ValueError) as ctx:
            A * B
        self.assertIn("dimension mismatch", str(ctx.exception).lower())

    def test_multiply_scalar(self):
        """Test scalar multiplication."""
        A = Matrix([[1, 2], [3, 4]])
        result = A * 2
        expected = Matrix([[2, 4], [6, 8]])
        self.assertEqual(result, expected)

    def test_multiply_scalar_float(self):
        """Test scalar multiplication with float."""
        A = Matrix([[1, 2], [3, 4]])
        result = A * 0.5
        expected = Matrix([[0.5, 1.0], [1.5, 2.0]])
        self.assertEqual(result, expected)

    def test_rmultiply_scalar(self):
        """Test right multiplication by scalar."""
        A = Matrix([[1, 2], [3, 4]])
        result = 3 * A
        expected = Matrix([[3, 6], [9, 12]])
        self.assertEqual(result, expected)

    def test_multiply_zero_matrix(self):
        """Test multiplication with zero matrix."""
        A = Matrix([[1, 2], [3, 4]])
        Z = Matrix([[0, 0], [0, 0]])
        result = A * Z
        expected = Matrix([[0, 0], [0, 0]])
        self.assertEqual(result, expected)

    def test_multiply_column_vector(self):
        """Test multiplication with column vector."""
        A = Matrix([[1, 2], [3, 4]])  # 2x2
        v = Matrix([[5], [6]])  # 2x1
        result = A * v
        expected = Matrix([[17], [39]])
        self.assertEqual(result, expected)

    def test_multiply_row_vector(self):
        """Test multiplication with row vector."""
        A = Matrix([[1, 2, 3]])  # 1x3
        v = Matrix([[4], [5], [6]])  # 3x1
        result = A * v
        self.assertEqual(result.rows, 1)
        self.assertEqual(result.cols, 1)
        self.assertAlmostEqual(result.data[0][0], 32)


class TestMatrixTranspose(unittest.TestCase):
    """Test matrix transpose."""

    def test_transpose_square(self):
        """Test transpose of square matrix."""
        A = Matrix([[1, 2], [3, 4]])
        result = A.transpose()
        expected = Matrix([[1, 3], [2, 4]])
        self.assertEqual(result, expected)

    def test_transpose_rectangular(self):
        """Test transpose of rectangular matrix."""
        A = Matrix([[1, 2, 3], [4, 5, 6]])  # 2x3
        result = A.transpose()
        expected = Matrix([[1, 4], [2, 5], [3, 6]])  # 3x2
        self.assertEqual(result, expected)

    def test_transpose_twice(self):
        """Test that transposing twice returns original."""
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        result = A.transpose().transpose()
        self.assertEqual(result, A)

    def test_transpose_column_vector(self):
        """Test transpose of column vector."""
        v = Matrix([[1], [2], [3]])
        result = v.transpose()
        expected = Matrix([[1, 2, 3]])
        self.assertEqual(result, expected)

    def test_transpose_row_vector(self):
        """Test transpose of row vector."""
        v = Matrix([[1, 2, 3]])
        result = v.transpose()
        expected = Matrix([[1], [2], [3]])
        self.assertEqual(result, expected)

    def test_transpose_1x1(self):
        """Test transpose of 1x1 matrix."""
        A = Matrix([[5]])
        result = A.transpose()
        self.assertEqual(result, A)


class TestMatrixDeterminant(unittest.TestCase):
    """Test determinant calculation."""

    def test_det_1x1(self):
        """Test determinant of 1x1 matrix."""
        A = Matrix([[5]])
        self.assertEqual(A.determinant(), 5)

    def test_det_2x2(self):
        """Test determinant of 2x2 matrix."""
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A.determinant(), -2)

    def test_det_3x3(self):
        """Test determinant of 3x3 matrix."""
        A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(A.determinant(), 0)  # Singular

    def test_det_3x3_non_singular(self):
        """Test determinant of non-singular 3x3 matrix."""
        A = Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
        self.assertEqual(A.determinant(), 4)

    def test_det_4x4(self):
        """Test determinant of 4x4 matrix."""
        A = Matrix([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
        self.assertEqual(A.determinant(), 24)

    def test_det_identity(self):
        """Test determinant of identity matrix."""
        I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertEqual(I.determinant(), 1)

    def test_det_zero_matrix(self):
        """Test determinant of zero matrix."""
        Z = Matrix([[0, 0], [0, 0]])
        self.assertEqual(Z.determinant(), 0)

    def test_det_not_square(self):
        """Test that non-square matrix raises ValueError."""
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            A.determinant()

    def test_det_empty(self):
        """Test that empty matrix raises ValueError."""
        A = Matrix([[]])
        with self.assertRaises(ValueError):
            A.determinant()


class TestMatrixInverse(unittest.TestCase):
    """Test matrix inversion."""

    def test_inverse_2x2(self):
        """Test inverse of 2x2 matrix."""
        A = Matrix([[1, 2], [3, 4]])
        inv = A.inverse()
        self.assertIsNotNone(inv)
        # Verify A * A^-1 = I
        identity = A * inv
        I = Matrix([[1, 0], [0, 1]])
        self.assertEqual(identity, I)

    def test_inverse_3x3(self):
        """Test inverse of 3x3 matrix."""
        A = Matrix([[1, 0, 1], [0, 1, 0], [0, 0, 1]])
        inv = A.inverse()
        self.assertIsNotNone(inv)
        identity = A * inv
        I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertEqual(identity, I)

    def test_inverse_singular(self):
        """Test that singular matrix returns None."""
        A = Matrix([[1, 2], [2, 4]])  # Determinant = 0
        inv = A.inverse()
        self.assertIsNone(inv)

    def test_inverse_not_square(self):
        """Test that non-square matrix raises ValueError."""
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            A.inverse()

    def test_inverse_empty(self):
        """Test that empty matrix raises ValueError."""
        A = Matrix([[]])
        with self.assertRaises(ValueError):
            A.inverse()

    def test_inverse_identity(self):
        """Test that inverse of identity is identity."""
        I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        inv = I.inverse()
        self.assertIsNotNone(inv)
        self.assertEqual(inv, I)

    def test_inverse_1x1(self):
        """Test inverse of 1x1 matrix."""
        A = Matrix([[5]])
        inv = A.inverse()
        self.assertIsNotNone(inv)
        self.assertEqual(inv.data[0][0], 0.2)

    def test_inverse_numerical_precision(self):
        """Test inverse with floating point values."""
        A = Matrix([[1.5, 2.5], [3.5, 4.5]])
        inv = A.inverse()
        self.assertIsNotNone(inv)
        identity = A * inv
        I = Matrix([[1, 0], [0, 1]])
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(identity.data[i][j], I.data[i][j], places=10)


class TestScalarOperations(unittest.TestCase):
    """Test scalar operations."""

    def test_scalar_multiply_positive(self):
        """Test scalar multiplication with positive scalar."""
        A = Matrix([[1, 2], [3, 4]])
        result = scalar_multiply(A, 3)
        expected = Matrix([[3, 6], [9, 12]])
        self.assertEqual(result, expected)

    def test_scalar_multiply_negative(self):
        """Test scalar multiplication with negative scalar."""
        A = Matrix([[1, 2], [3, 4]])
        result = scalar_multiply(A, -2)
        expected = Matrix([[-2, -4], [-6, -8]])
        self.assertEqual(result, expected)

    def test_scalar_multiply_zero(self):
        """Test scalar multiplication with zero."""
        A = Matrix([[1, 2], [3, 4]])
        result = scalar_multiply(A, 0)
        expected = Matrix([[0, 0], [0, 0]])
        self.assertEqual(result, expected)

    def test_scalar_multiply_fraction(self):
        """Test scalar multiplication with fractional scalar."""
        A = Matrix([[2, 4], [6, 8]])
        result = scalar_multiply(A, 0.5)
        expected = Matrix([[1, 2], [3, 4]])
        self.assertEqual(result, expected)

    def test_scalar_multiply_large(self):
        """Test scalar multiplication with large scalar."""
        A = Matrix([[1, 2], [3, 4]])
        result = scalar_multiply(A, 1000)
        expected = Matrix([[1000, 2000], [3000, 4000]])
        self.assertEqual(result, expected)


class TestParseMatrixString(unittest.TestCase):
    """Test matrix string parsing."""

    def test_parse_semicolon(self):
        """Test parsing with semicolon delimiter."""
        s = "1 2 3; 4 5 6"
        m = parse_matrix_string(s)
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 3)
        self.assertEqual(m.data, [[1, 2, 3], [4, 5, 6]])

    def test_parse_comma(self):
        """Test parsing with comma delimiter."""
        s = "1,2,3;4,5,6"
        m = parse_matrix_string(s)
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 3)
        self.assertEqual(m.data, [[1, 2, 3], [4, 5, 6]])

    def test_parse_floats(self):
        """Test parsing floating point numbers."""
        s = "1.5 2.5; 3.5 4.5"
        m = parse_matrix_string(s)
        self.assertEqual(m.data, [[1.5, 2.5], [3.5, 4.5]])

    def test_parse_scientific(self):
        """Test parsing scientific notation."""
        s = "1e2 2e-1; 3 4e2"
        m = parse_matrix_string(s)
        self.assertEqual(m.data[0][0], 100)
        self.assertAlmostEqual(m.data[0][1], 0.2)
        self.assertEqual(m.data[1][0], 3)
        self.assertEqual(m.data[1][1], 400)

    def test_parse_single_row(self):
        """Test parsing single row."""
        s = "1 2 3 4 5"
        m = parse_matrix_string(s)
        self.assertEqual(m.rows, 1)
        self.assertEqual(m.cols, 5)

    def test_parse_single_column(self):
        """Test parsing single column."""
        s = "1; 2; 3; 4"
        m = parse_matrix_string(s)
        self.assertEqual(m.rows, 4)
        self.assertEqual(m.cols, 1)

    def test_parse_empty_string(self):
        """Test that empty string raises ValueError."""
        with self.assertRaises(ValueError):
            parse_matrix_string("")

    def test_parse_inconsistent_rows(self):
        """Test that inconsistent rows raise ValueError."""
        s = "1 2; 3 4 5"
        with self.assertRaises(ValueError):
            parse_matrix_string(s)

    def test_parse_invalid_number(self):
        """Test that invalid number raises ValueError."""
        s = "1 abc 3; 4 5 6"
        with self.assertRaises(ValueError):
            parse_matrix_string(s)

    def test_parse_negative_numbers(self):
        """Test parsing negative numbers."""
        s = "-1 -2; -3 -4"
        m = parse_matrix_string(s)
        self.assertEqual(m.data, [[-1, -2], [-3, -4]])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""

    def test_zero_matrix_determinant(self):
        """Test determinant of zero matrix."""
        Z = Matrix([[0, 0], [0, 0]])
        self.assertEqual(Z.determinant(), 0)

    def test_zero_matrix_inverse(self):
        """Test inverse of zero matrix returns None."""
        Z = Matrix([[0, 0], [0, 0]])
        self.assertIsNone(Z.inverse())

    def test_large_matrix_operations(self):
        """Test operations on larger matrices."""
        A = Matrix([[i + j for j in range(5)] for i in range(5)])
        B = Matrix([[i * j for j in range(5)] for i in range(5)])
        result = A + B
        self.assertEqual(result.rows, 5)
        self.assertEqual(result.cols, 5)

    def test_identity_properties(self):
        """Test identity matrix properties."""
        I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        A = Matrix([[2, 3, 4], [5, 6, 7], [8, 9, 10]])
        # I * A = A
        self.assertEqual(I * A, A)
        # A * I = A
        self.assertEqual(A * I, A)
        # I^T = I
        self.assertEqual(I.transpose(), I)

    def test_transpose_of_zero_matrix(self):
        """Test transpose of zero matrix."""
        Z = Matrix([[0, 0, 0], [0, 0, 0]])
        ZT = Z.transpose()
        self.assertEqual(ZT, Matrix([[0, 0], [0, 0], [0, 0]]))

    def test_scalar_zero_preserves_zero(self):
        """Test that multiplying zero matrix by scalar yields zero."""
        Z = Matrix([[0, 0], [0, 0]])
        result = Z * 5
        self.assertEqual(result, Z)

    def test_negative_scalar_inverse(self):
        """Test that A * (-1) gives negation."""
        A = Matrix([[1, 2], [3, 4]])
        neg = A * -1
        expected = Matrix([[-1, -2], [-3, -4]])
        self.assertEqual(neg, expected)

    def test_associativity_addition(self):
        """Test associativity of addition: (A+B)+C = A+(B+C)."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = Matrix([[9, 10], [11, 12]])
        left = (A + B) + C
        right = A + (B + C)
        self.assertEqual(left, right)

    def test_distributivity(self):
        """Test distributivity: A*(B+C) = A*B + A*C."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = Matrix([[9, 10], [11, 12]])
        left = A * (B + C)
        right = A * B + A * C
        self.assertEqual(left, right)

    def test_transpose_of_sum(self):
        """Test (A+B)^T = A^T + B^T."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        left = (A + B).transpose()
        right = A.transpose() + B.transpose()
        self.assertEqual(left, right)

    def test_determinant_of_product(self):
        """Test det(AB) = det(A) * det(B) for 2x2 matrices."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        det_AB = (A * B).determinant()
        det_A = A.determinant()
        det_B = B.determinant()
        self.assertAlmostEqual(det_AB, det_A * det_B, places=10)


class TestStandaloneFunctions(unittest.TestCase):
    """Test standalone convenience functions."""

    def test_matrix_add_function(self):
        """Test matrix_add function."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        result = matrix_add(A, B)
        self.assertEqual(result, A + B)

    def test_matrix_subtract_function(self):
        """Test matrix_subtract function."""
        A = Matrix([[5, 6], [7, 8]])
        B = Matrix([[1, 2], [3, 4]])
        result = matrix_subtract(A, B)
        self.assertEqual(result, A - B)

    def test_matrix_multiply_function(self):
        """Test matrix_multiply function."""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        result = matrix_multiply(A, B)
        self.assertEqual(result, A * B)

    def test_matrix_transpose_function(self):
        """Test matrix_transpose function."""
        A = Matrix([[1, 2], [3, 4]])
        result = matrix_transpose(A)
        self.assertEqual(result, A.transpose())

    def test_matrix_determinant_function(self):
        """Test matrix_determinant function."""
        A = Matrix([[1, 2], [3, 4]])
        result = matrix_determinant(A)
        self.assertEqual(result, A.determinant())

    def test_matrix_inverse_function(self):
        """Test matrix_inverse function."""
        A = Matrix([[1, 2], [3, 4]])
        result = matrix_inverse(A)
        self.assertEqual(result, A.inverse())

    def test_scalar_multiply_function(self):
        """Test scalar_multiply function."""
        A = Matrix([[1, 2], [3, 4]])
        result = scalar_multiply(A, 2)
        expected = Matrix([[2, 4], [6, 8]])
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
