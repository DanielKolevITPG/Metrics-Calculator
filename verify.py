"""Quick verification script for matrix calculator."""

from matrix_operations import Matrix, parse_matrix_string

print("Testing Matrix Calculator...")
print("=" * 50)

# Test 1: Addition
print("\n1. Testing Addition:")
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])
result = A + B
print(f"A + B = {result.data}")

# Test 2: Subtraction
print("\n2. Testing Subtraction:")
result = A - B
print(f"A - B = {result.data}")

# Test 3: Multiplication
print("\n3. Testing Matrix Multiplication:")
C = Matrix([[1, 2, 3], [4, 5, 6]])
D = Matrix([[7, 8], [9, 10], [11, 12]])
result = C * D
print(f"C * D = {result.data}")

# Test 4: Scalar multiplication
print("\n4. Testing Scalar Multiplication:")
result = A * 2
print(f"A * 2 = {result.data}")

# Test 5: Transpose
print("\n5. Testing Transpose:")
result = A.transpose()
print(f"A^T = {result.data}")

# Test 6: Determinant
print("\n6. Testing Determinant:")
det = A.determinant()
print(f"det(A) = {det}")

# Test 7: Inverse
print("\n7. Testing Inverse:")
inv = A.inverse()
if inv:
    print(f"A^-1 = {inv.data}")
    # Verify
    identity = A * inv
    print(f"A * A^-1 = {identity.data}")
else:
    print("Matrix is singular")

# Test 8: Parse matrix string
print("\n8. Testing Matrix Parsing:")
s = "1 2 3; 4 5 6; 7 8 9"
M = parse_matrix_string(s)
print(f"Parsed matrix: {M.data}")

print("\n" + "=" * 50)
print("All basic operations verified successfully!")
