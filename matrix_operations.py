"""
Matrix operations module providing fundamental matrix arithmetic and transformations.

This module implements a Matrix class with support for:
- Addition and subtraction
- Matrix multiplication (dot product)
- Determinant calculation
- Matrix inversion
- Transpose
- Scalar operations

All operations include comprehensive error handling and validation.
"""

from __future__ import annotations
from typing import List, Optional
import copy


class Matrix:
    """A class representing a mathematical matrix with various operations."""

    def __init__(self, data: List[List[float]]):
        """
        Initialize a matrix from a list of lists.

        Args:
            data: 2D list representing matrix rows

        Raises:
            TypeError: If data is not a list of lists
            ValueError: If rows have inconsistent lengths
        """
        if not isinstance(data, list):
            raise TypeError("Matrix data must be a list of lists")

        if not all(isinstance(row, list) for row in data):
            raise TypeError("Matrix data must be a list of lists")

        # Check for consistent row lengths
        if len(data) > 0:
            row_length = len(data[0])
            for i, row in enumerate(data):
                if len(row) != row_length:
                    raise ValueError(
                        f"Row {i} has length {len(row)}, expected {row_length}"
                    )

        self.data = copy.deepcopy(data)
        self.rows = len(data)
        self.cols = len(data[0]) if len(data) > 0 else 0

    def __repr__(self) -> str:
        return f"Matrix({self.data})"

    def __str__(self) -> str:
        return self._format_matrix()

    def _format_matrix(self) -> str:
        """Format matrix for display with proper alignment."""
        if self.rows == 0 or self.cols == 0:
            return "[]"

        # Convert all elements to strings and find max width
        str_data = [[str(element) for element in row] for row in self.data]
        max_width = max(len(str_elem) for row in str_data for str_elem in row)

        lines = []
        for row in str_data:
            formatted_row = " ".join(f"{elem:>{max_width}}" for elem in row)
            lines.append(f"[{formatted_row}]")

        return "\n".join(lines)

    def __eq__(self, other: object) -> bool:
        """Check equality with another matrix (with tolerance for floating point)."""
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(
            abs(self.data[i][j] - other.data[i][j]) < 1e-10
            for i in range(self.rows)
            for j in range(self.cols)
        )

    def validate_square(self) -> None:
        """Validate that matrix is square."""
        if self.rows != self.cols:
            raise ValueError(
                f"Operation requires a square matrix. Got {self.rows}x{self.cols}"
            )

    def validate_not_empty(self) -> None:
        """Validate that matrix is not empty."""
        if self.rows == 0 or self.cols == 0:
            raise ValueError("Operation requires a non-empty matrix")

    def __add__(self, other: Matrix) -> Matrix:
        """Add two matrices (A + B)."""
        if not isinstance(other, Matrix):
            raise TypeError(f"Cannot add Matrix with {type(other).__name__}")

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Dimension mismatch for addition: "
                f"{self.rows}x{self.cols} + {other.rows}x{other.cols}"
            )

        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __sub__(self, other: Matrix) -> Matrix:
        """Subtract two matrices (A - B)."""
        if not isinstance(other, Matrix):
            raise TypeError(f"Cannot subtract Matrix with {type(other).__name__}")

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Dimension mismatch for subtraction: "
                f"{self.rows}x{self.cols} - {other.rows}x{other.cols}"
            )

        result = [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other: float | Matrix) -> Matrix:
        """
        Multiply matrix by scalar or perform matrix multiplication.

        Args:
            other: Scalar (int/float) or Matrix

        Returns:
            Matrix: Result of multiplication

        Raises:
            TypeError: If other is not scalar or Matrix
            ValueError: If matrix dimensions don't match for multiplication
        """
        if isinstance(other, (int, float)):
            result = [
                [self.data[i][j] * other for j in range(self.cols)]
                for i in range(self.rows)
            ]
            return Matrix(result)
        elif isinstance(other, Matrix):
            # Matrix multiplication (dot product)
            if self.cols != other.rows:
                raise ValueError(
                    f"Matrix multiplication dimension mismatch: "
                    f"{self.rows}x{self.cols} * {other.rows}x{other.cols}"
                )

            result = [
                [
                    sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
            return Matrix(result)
        else:
            raise TypeError(
                f"Unsupported operand type for *: 'Matrix' and '{type(other).__name__}'"
            )

    def __rmul__(self, other: float | int) -> Matrix:
        """Right multiplication by scalar."""
        return self.__mul__(other)

    def transpose(self) -> Matrix:
        """Return the transpose of the matrix."""
        result = [
            [self.data[i][j] for i in range(self.rows)] for j in range(self.cols)
        ]
        return Matrix(result)

    def determinant(self) -> float:
        """
        Calculate the determinant of the matrix.

        Returns:
            float: Determinant value

        Raises:
            ValueError: If matrix is not square or is empty
        """
        self.validate_not_empty()
        self.validate_square()

        # Use recursive Laplace expansion for small matrices
        if self.rows == 1:
            return self.data[0][0]

        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

        if self.rows == 3:
            # Sarrus' rule for 3x3
            a, b, c = self.data[0]
            d, e, f = self.data[1]
            g, h, i = self.data[2]
            return (
                a * e * i
                + b * f * g
                + c * d * h
                - c * e * g
                - b * d * i
                - a * f * h
            )

        # For larger matrices, use LU decomposition via Gaussian elimination
        return self._determinant_gaussian()

    def _determinant_gaussian(self) -> float:
        """Calculate determinant using Gaussian elimination (more efficient for n>3)."""
        n = self.rows
        # Create a copy to avoid modifying original
        matrix = copy.deepcopy(self.data)
        det = 1.0

        for i in range(n):
            # Find pivot
            pivot = i
            while pivot < n and abs(matrix[pivot][i]) < 1e-12:
                pivot += 1

            if pivot == n:
                return 0.0  # Singular matrix

            if pivot != i:
                # Swap rows
                matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
                det *= -1

            det *= matrix[i][i]

            # Eliminate
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]

        return det

    def inverse(self) -> Optional[Matrix]:
        """
        Calculate the inverse of the matrix using Gauss-Jordan elimination.

        Returns:
            Matrix: Inverse matrix if invertible
            None: If matrix is singular (determinant near zero)

        Raises:
            ValueError: If matrix is not square or is empty
        """
        self.validate_not_empty()
        self.validate_square()

        n = self.rows
        # Create augmented matrix [A | I]
        aug = copy.deepcopy(self.data)
        for i in range(n):
            aug[i] = aug[i] + [1.0 if i == j else 0.0 for j in range(n)]

        # Gauss-Jordan elimination
        for i in range(n):
            # Find pivot
            pivot = i
            while pivot < n and abs(aug[pivot][i]) < 1e-12:
                pivot += 1

            if pivot == n:
                return None  # Singular matrix

            if pivot != i:
                aug[i], aug[pivot] = aug[pivot], aug[i]

            # Normalize pivot row
            pivot_val = aug[i][i]
            if abs(pivot_val) < 1e-12:
                return None

            for j in range(2 * n):
                aug[i][j] /= pivot_val

            # Eliminate other rows
            for k in range(n):
                if k != i:
                    factor = aug[k][i]
                    for j in range(2 * n):
                        aug[k][j] -= factor * aug[i][j]

        # Extract inverse
        result = [row[n:] for row in aug]
        return Matrix(result)

    def copy(self) -> Matrix:
        """Create a deep copy of the matrix."""
        return Matrix(copy.deepcopy(self.data))


# Standalone functions for convenience
def matrix_add(A: Matrix, B: Matrix) -> Matrix:
    """Add two matrices."""
    return A + B


def matrix_subtract(A: Matrix, B: Matrix) -> Matrix:
    """Subtract matrix B from matrix A."""
    return A - B


def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """Multiply two matrices (dot product)."""
    return A * B


def scalar_multiply(A: Matrix, scalar: float) -> Matrix:
    """Multiply matrix by scalar."""
    return A * scalar


def matrix_transpose(A: Matrix) -> Matrix:
    """Return transpose of matrix."""
    return A.transpose()


def matrix_determinant(A: Matrix) -> float:
    """Calculate determinant of matrix."""
    return A.determinant()


def matrix_inverse(A: Matrix) -> Optional[Matrix]:
    """Calculate inverse of matrix."""
    return A.inverse()


def parse_matrix_string(s: str) -> Matrix:
    """
    Parse a matrix from a string representation.

    Format: "1 2 3; 4 5 6" where semicolons separate rows
    Alternative: "1,2,3;4,5,6" or "1 2 3,4 5 6"

    Args:
        s: String representation of matrix

    Returns:
        Matrix: Parsed matrix

    Raises:
        ValueError: If string format is invalid
    """
    if not s.strip():
        raise ValueError("Empty matrix string")

    # Split by semicolon to get rows
    rows_str = s.strip().split(";")
    data = []

    for row_str in rows_str:
        row_str = row_str.strip()
        if not row_str:
            raise ValueError("Empty row in matrix string")

        # Try different delimiters
        if "," in row_str:
            elements = row_str.split(",")
        else:
            elements = row_str.split()

        # Convert to numbers
        row = []
        for elem in elements:
            elem = elem.strip()
            if not elem:
                raise ValueError("Empty element in matrix")
            try:
                # Try integer first, then float
                if "." in elem or "e" in elem.lower():
                    row.append(float(elem))
                else:
                    row.append(int(elem))
            except ValueError:
                raise ValueError(f"Invalid number: '{elem}'")

        data.append(row)

    # Validate consistent row lengths
    if len(data) > 0:
        row_len = len(data[0])
        for i, row in enumerate(data):
            if len(row) != row_len:
                raise ValueError(
                    f"Inconsistent row lengths: row 0 has {row_len}, row {i} has {len(row)}"
                )

    return Matrix(data)
