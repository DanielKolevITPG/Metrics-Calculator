# Matrix Calculator

A fully functional matrix calculator implemented in Python 3.11+ with comprehensive test coverage.

## Files

- `src/matrix_calculator/matrix_operations.py` - Core matrix operations module
- `src/matrix_calculator/ui.py` - Tkinter UI
- `src/matrix_calculator/cli.py` - Menu-driven CLI interface
- `main.py` - Workspace launcher (UI by default)
- `tests/test_matrix_operations.py` - Comprehensive test suite
- `requirements.txt` - Optional dependencies
- `verify.py` - Quick verification script

## Installation

No external dependencies required for core operations.

For the UI extras (Eigen/Random features), install the optional numpy extra.

```bash
# Optional: install package in editable mode
pip install -e .

# Optional: UI extras (Eigen/Random)
pip install -e .[ui]
```

## Usage

### Running the UI (default)

```bash
python main.py
```

You can also run after installation:

```bash
matrix-calculator
```

### Running the CLI

```bash
python main.py --cli
```

Or after installation:

```bash
matrix-calculator-cli
```

This launches an interactive menu-driven interface with the following options:

1. **Add matrices (A + B)** - Adds two matrices of same dimensions
2. **Subtract matrices (A - B)** - Subtracts matrix B from matrix A
3. **Multiply matrices (A * B)** - Performs matrix multiplication (dot product)
4. **Calculate determinant** - Computes determinant of a square matrix
5. **Calculate inverse** - Computes inverse of a square matrix (returns None if singular)
6. **Transpose matrix** - Returns transpose of a matrix
7. **Scalar multiplication** - Multiplies matrix by a scalar value
8. **Exit** - Quits the program

### Matrix Input Format

Enter matrices using the format: `"1 2 3; 4 5 6"`

- Semicolons (`;`) separate rows
- Spaces or commas separate elements within a row
- Examples:
  - `"1 2 3; 4 5 6"` creates a 2x3 matrix
  - `"1,2,3;4,5,6"` also works
  - `"1 2 3 4 5"` creates a 1x5 row vector
  - `"1; 2; 3; 4"` creates a 4x1 column vector

### Expected Output Examples

#### Menu Display
```
==================================================
MATRIX CALCULATOR
==================================================
1. Add matrices (A + B)
2. Subtract matrices (A - B)
3. Multiply matrices (A * B)
4. Calculate determinant
5. Calculate inverse
6. Transpose matrix
7. Scalar multiplication
8. Exit
==================================================
```

#### Addition Example
```
Enter first matrix (A)
Format: '1 2 3; 4 5 6' (semicolons separate rows)
...
Matrix:
[1 2]
[3 4]

Enter second matrix (B)
...
Matrix:
[5 6]
[7 8]

Proceed? (y/n): y

Result (A + B):
[6 8]
[10 12]
```

#### Determinant Example
```
Enter matrix
...
Matrix:
[1 2]
[3 4]

Proceed? (y/n): y

Determinant: -2
```

#### Inverse Example
```
Enter matrix
...
Matrix:
[1 2]
[3 4]

Proceed? (y/n): y

Inverse:
[-2.0 1.0]
[1.5 -0.5]

Verification (A * A^-1):
[1.0 0.0]
[0.0 1.0]
```

#### Error Handling
The program handles errors gracefully:
- Dimension mismatches: "Error: Dimension mismatch for addition: 2x2 + 3x3"
- Non-square for determinant/inverse: "Error: Operation requires a square matrix. Got 2x3"
- Singular matrices: "Error: Matrix is singular (non-invertible)"
- Invalid input: "Error: Invalid number: 'abc'"

## Running Tests

### Using unittest (standard library)

```bash
python -m unittest tests/test_matrix_operations.py -v
```

Expected output:
```
test_add_1x1 (test.TestMatrixAddition.test_add_1x1) ... ok
test_add_column_vector (test.TestMatrixAddition.test_add_column_vector) ... ok
...
----------------------------------------------------------------------
Ran 84 tests in 0.003s

OK
```

### Test Coverage

The test suite includes:
- **Initialization tests** (6 tests) - Matrix creation, validation, deep copy
- **Addition tests** (8 tests) - Basic addition, dimension mismatches, edge cases
- **Subtraction tests** (4 tests) - Basic and edge cases
- **Multiplication tests** (11 tests) - Matrix multiplication, scalar operations, vectors
- **Transpose tests** (5 tests) - Square, rectangular, vectors
- **Determinant tests** (9 tests) - 1x1 through 4x4, edge cases, error handling
- **Inverse tests** (8 tests) - Invertible matrices, singular, numerical precision
- **Scalar operations tests** (5 tests) - Various scalar values
- **Parsing tests** (10 tests) - String parsing, formats, validation
- **Edge cases tests** (13 tests) - Identity properties, associativity, distributivity
- **Standalone functions tests** (8 tests) - Convenience function wrappers

**Total: 84 tests, all passing**

### Using pytest (optional)

```bash
pytest tests/test_matrix_operations.py -v
```

## Quick Verification

Run the verification script to see all operations in action:

```bash
python verify.py
```

Expected output shows successful execution of:
- Addition
- Subtraction
- Matrix multiplication
- Scalar multiplication
- Transpose
- Determinant
- Inverse with verification
- Matrix parsing

## Implementation Details

### Matrix Class

The `Matrix` class in `matrix_operations.py` provides:

- **Storage**: List of lists representation
- **Operations**:
  - `__add__`, `__sub__` - Element-wise addition/subtraction
  - `__mul__` - Matrix multiplication or scalar multiplication
  - `transpose()` - Matrix transpose
  - `determinant()` - Determinant via Laplace expansion (n≤3) or Gaussian elimination (n>3)
  - `inverse()` - Gauss-Jordan elimination, returns None for singular matrices
- **Validation**: Comprehensive error checking for dimensions, types, and edge cases
- **Formatting**: Pretty-print with proper alignment

### Error Handling

All operations raise appropriate exceptions:
- `TypeError` - Invalid operand types
- `ValueError` - Dimension mismatches, non-square matrices, empty matrices, singular matrices

### Numerical Precision

- Uses Gaussian elimination with partial pivoting for determinant
- Gauss-Jordan elimination for inverse with tolerance `1e-12` for singularity detection
- `assertAlmostEqual` used in tests for floating-point comparisons

## Python Version

Requires Python 3.11+ (uses type hints and modern syntax)

## Project Structure

```
c:/Users/Students/Project/
├── matrix_operations.py   # Core operations
├── main.py               # CLI interface
├── test.py               # Test suite
├── requirements.txt      # Dependencies (empty)
├── verify.py            # Quick verification
└── README.md            # This file
```

## Examples

### Example 1: Matrix Multiplication
```
Input: A = "1 2; 3 4", B = "5 6; 7 8"
Result: [[19, 22], [43, 50]]
```

### Example 2: Determinant
```
Input: "2 -1 0; -1 2 -1; 0 -1 2"
Result: 4
```

### Example 3: Inverse
```
Input: "1 0 1; 0 1 0; 0 0 1"
Result:
[1.0 0.0 -1.0]
[0.0 1.0 0.0]
[0.0 0.0 1.0]
```

### Example 4: Transpose
```
Input: "1 2 3; 4 5 6"
Result:
[1 4]
[2 5]
[3 6]
```

## Notes

- The implementation is self-contained and does not use external matrix libraries for core operations
- The `inverse()` method returns `None` for singular matrices instead of raising an exception
- Determinant calculation uses optimized formulas for 1x1, 2x2, and 3x3 matrices, and Gaussian elimination for larger matrices
- All operations support edge cases: empty matrices, 1x1, 1xn, nx1, zero matrices
- The CLI includes confirmation prompts and allows retry on invalid input

## License

Educational project - free to use and modify.
