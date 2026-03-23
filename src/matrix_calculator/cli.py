"""Menu-driven CLI for matrix operations."""

from __future__ import annotations

import sys

from .matrix_operations import Matrix, parse_matrix_string


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("MATRIX CALCULATOR")
    print("=" * 50)
    print("1. Add matrices (A + B)")
    print("2. Subtract matrices (A - B)")
    print("3. Multiply matrices (A * B)")
    print("4. Calculate determinant")
    print("5. Calculate inverse")
    print("6. Transpose matrix")
    print("7. Scalar multiplication")
    print("8. Exit")
    print("=" * 50)


def input_matrix(prompt: str) -> Matrix:
    """Prompt user to input a matrix."""
    print(f"\n{prompt}")
    print("Format: '1 2 3; 4 5 6' (semicolons separate rows)")
    print("       or '1,2,3;4,5,6' (commas optional)")
    print("Example: '1 2 3; 4 5 6; 7 8 9' for a 3x3 matrix")
    print("Enter empty string to cancel")

    while True:
        try:
            s = input("\nMatrix: ").strip()
            if not s:
                raise ValueError("Operation cancelled")

            matrix = parse_matrix_string(s)
            print(f"Parsed matrix ({matrix.rows}x{matrix.cols}):")
            print(matrix)
            return matrix
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again or enter empty string to cancel.")
            retry = input("Retry? (y/n): ").strip().lower()
            if retry != "y":
                raise ValueError("Operation cancelled")


def input_scalar(prompt: str) -> float:
    """Prompt user to input a scalar value."""
    print(f"\n{prompt}")
    while True:
        s = ""
        try:
            s = input("Scalar value: ").strip()
            if not s:
                raise ValueError("Operation cancelled")
            return float(s)
        except ValueError as e:
            if str(e) == "Operation cancelled":
                raise
            print(f"Error: Invalid number '{s}'")
            print("Please try again or enter empty string to cancel.")
            retry = input("Retry? (y/n): ").strip().lower()
            if retry != "y":
                raise ValueError("Operation cancelled")


def confirm_operation(description: str) -> bool:
    """Ask user to confirm the operation."""
    print(f"\n{description}")
    response = input("Proceed? (y/n): ").strip().lower()
    return response == "y"


def pause() -> None:
    """Pause and wait for user to press Enter."""
    try:
        input("\nPress Enter to continue...")
    except EOFError:
        # Non-interactive invocation (e.g. piping/CI) shouldn't crash.
        return


def run_cli() -> None:
    """Run the CLI main loop."""
    print("Welcome to the Matrix Calculator!")

    while True:
        display_menu()

        try:
            try:
                choice = input("\nEnter your choice (1-8): ").strip()
            except EOFError:
                # Non-interactive invocation: exit cleanly.
                return

            if choice == "1":
                A = input_matrix("Enter first matrix (A)")
                B = input_matrix("Enter second matrix (B)")
                if confirm_operation(f"Computing A + B:\n{A}\n+\n{B}"):
                    result = A + B
                    print("\nResult (A + B):")
                    print(result)

            elif choice == "2":
                A = input_matrix("Enter first matrix (A)")
                B = input_matrix("Enter second matrix (B)")
                if confirm_operation(f"Computing A - B:\n{A}\n-\n{B}"):
                    result = A - B
                    print("\nResult (A - B):")
                    print(result)

            elif choice == "3":
                A = input_matrix("Enter first matrix (A)")
                B = input_matrix("Enter second matrix (B)")
                if confirm_operation(
                    f"Computing A * B (matrix multiplication):\n{A}\n*\n{B}"
                ):
                    result = A * B
                    print("\nResult (A * B):")
                    print(result)

            elif choice == "4":
                A = input_matrix("Enter matrix")
                if confirm_operation(f"Calculating determinant of:\n{A}"):
                    det = A.determinant()
                    print(f"\nDeterminant: {det}")

            elif choice == "5":
                A = input_matrix("Enter matrix")
                if confirm_operation(f"Calculating inverse of:\n{A}"):
                    inv = A.inverse()
                    if inv is None:
                        print("\nError: Matrix is singular (non-invertible)")
                    else:
                        print("\nInverse:")
                        print(inv)
                        identity = A * inv
                        print("\nVerification (A * A^-1):")
                        print(identity)

            elif choice == "6":
                A = input_matrix("Enter matrix")
                if confirm_operation(f"Transposing:\n{A}"):
                    result = A.transpose()
                    print("\nTranspose:")
                    print(result)

            elif choice == "7":
                A = input_matrix("Enter matrix")
                scalar = input_scalar("Enter scalar value")
                if confirm_operation(f"Computing {scalar} * A:"):
                    result = A * scalar
                    print(f"\nResult ({scalar} * A):")
                    print(result)

            elif choice == "8":
                print("\nThank you for using Matrix Calculator. Goodbye!")
                sys.exit(0)

            else:
                print("Invalid choice. Please enter a number between 1 and 8.")

        except ValueError as e:
            if str(e) != "Operation cancelled":
                print(f"\nError: {e}")
        except Exception as e:
            print(f"\nUnexpected error: {e}")

        pause()
