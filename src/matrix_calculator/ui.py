"""Tkinter UI for the matrix calculator.

Improved usability vs the original:
- ttk widgets + cleaner layout
- spinboxes for dimensions with sensible defaults
- blank cells treated as 0
- clearer error messages that point to the exact cell
- scrollable, monospace output
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    np = None

from .matrix_operations import Matrix
from . import matrix_operations as mo


class MatrixCalculatorUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Matrix Calculator")
        self.root.minsize(860, 560)
        self.root.geometry("980x640")

        try:
            style = ttk.Style(self.root)
            if "clam" in style.theme_names():
                style.theme_use("clam")
        except Exception:
            pass

        self._ui_font = ("Segoe UI", 10)
        self._mono_font = ("Consolas", 10)
        self.root.option_add("*Font", self._ui_font)

        self.entries_A: list[list[ttk.Entry]] = []
        self.entries_B: list[list[ttk.Entry]] = []

        self.status_var = tk.StringVar(value="Ready")
        self.rows_A_var = tk.IntVar(value=2)
        self.cols_A_var = tk.IntVar(value=2)
        self.rows_B_var = tk.IntVar(value=2)
        self.cols_B_var = tk.IntVar(value=2)

        self._build_layout()
        self._build_dimension_controls()
        self._build_matrix_frames()
        self._build_buttons()
        self._build_result_area()

        self.create_matrices()

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(4, weight=1)

        self.top = ttk.Frame(self.root, padding=(12, 12, 12, 8))
        self.top.grid(row=0, column=0, sticky="ew")
        self.mid = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        self.mid.grid(row=1, column=0, sticky="ew")
        self.matrices = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        self.matrices.grid(row=2, column=0, sticky="nsew")
        self.actions = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        self.actions.grid(row=3, column=0, sticky="ew")
        self.out = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        self.out.grid(row=4, column=0, sticky="nsew")

        title = ttk.Label(
            self.top, text="Matrix Calculator", font=("Segoe UI Semibold", 16)
        )
        subtitle = ttk.Label(
            self.top,
            text="Enter values, then run an operation. Blank cells count as 0.",
            foreground="#444444",
        )
        status = ttk.Label(self.top, textvariable=self.status_var, foreground="#444444")
        title.grid(row=0, column=0, sticky="w")
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))
        status.grid(row=0, column=1, rowspan=2, sticky="e")
        self.top.columnconfigure(0, weight=1)

    def _build_dimension_controls(self) -> None:
        frame = ttk.LabelFrame(self.mid, text="Dimensions", padding=10)
        frame.grid(row=0, column=0, sticky="ew")
        self.mid.columnconfigure(0, weight=1)

        ttk.Label(frame, text="A").grid(row=0, column=0, sticky="e", padx=(0, 6))
        ttk.Label(frame, text="Rows").grid(row=0, column=1, sticky="w")
        ttk.Spinbox(frame, from_=1, to=12, textvariable=self.rows_A_var, width=5).grid(
            row=0, column=2, sticky="w", padx=(4, 14)
        )
        ttk.Label(frame, text="Cols").grid(row=0, column=3, sticky="w")
        ttk.Spinbox(frame, from_=1, to=12, textvariable=self.cols_A_var, width=5).grid(
            row=0, column=4, sticky="w", padx=(4, 18)
        )

        ttk.Label(frame, text="B").grid(row=0, column=5, sticky="e", padx=(0, 6))
        ttk.Label(frame, text="Rows").grid(row=0, column=6, sticky="w")
        ttk.Spinbox(frame, from_=1, to=12, textvariable=self.rows_B_var, width=5).grid(
            row=0, column=7, sticky="w", padx=(4, 14)
        )
        ttk.Label(frame, text="Cols").grid(row=0, column=8, sticky="w")
        ttk.Spinbox(frame, from_=1, to=12, textvariable=self.cols_B_var, width=5).grid(
            row=0, column=9, sticky="w", padx=(4, 18)
        )

        ttk.Button(frame, text="Create / Reset", command=self.create_matrices).grid(
            row=0, column=10, sticky="w"
        )
        ttk.Button(frame, text="Copy A -> B", command=self._copy_A_to_B_dims).grid(
            row=0, column=11, sticky="w", padx=(8, 0)
        )
        frame.columnconfigure(12, weight=1)

    def _build_matrix_frames(self) -> None:
        self.matrices.columnconfigure(0, weight=1)
        self.matrices.columnconfigure(1, weight=1)
        self.matrices.rowconfigure(0, weight=1)

        self.frame_A = ttk.LabelFrame(self.matrices, text="Matrix A", padding=10)
        self.frame_A.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.frame_B = ttk.LabelFrame(self.matrices, text="Matrix B", padding=10)
        self.frame_B.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    def _build_buttons(self) -> None:
        frame = ttk.LabelFrame(self.actions, text="Operations", padding=10)
        frame.grid(row=0, column=0, sticky="ew")
        self.actions.columnconfigure(0, weight=1)

        buttons = [
            ("A + B", self.add),
            ("A - B", self.subtract),
            ("A x B", self.multiply),
            ("Scalar x A", self.scalar),
            ("Transpose A", self.transpose),
            ("Determinant A", self.det),
            ("Inverse A", self.inverse),
            ("Trace A", self.trace),
            ("Rank A", self.rank),
            ("Eigen A", self.eigen),
            ("Random A", self.random_A),
            ("Clear", self.clear),
        ]

        for i, (label, cmd) in enumerate(buttons):
            r = i // 4
            c = i % 4
            ttk.Button(frame, text=label, command=cmd).grid(
                row=r, column=c, padx=4, pady=4, sticky="ew"
            )

        for c in range(4):
            frame.columnconfigure(c, weight=1)

    def _build_result_area(self) -> None:
        frame = ttk.LabelFrame(self.out, text="Output", padding=10)
        frame.grid(row=0, column=0, sticky="nsew")
        self.out.columnconfigure(0, weight=1)
        self.out.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.result = tk.Text(
            frame,
            height=10,
            wrap="none",
            font=self._mono_font,
            padx=10,
            pady=8,
        )
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.result.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=self.result.xview)
        self.result.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.result.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        self._set_result("Ready. Matrices are initialized to 0.")

    def _set_result(self, text: str) -> None:
        self.result.configure(state="normal")
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, text)
        self.result.configure(state="disabled")

    def _copy_A_to_B_dims(self) -> None:
        self.rows_B_var.set(self.rows_A_var.get())
        self.cols_B_var.set(self.cols_A_var.get())
        self.create_matrices()

    def create_matrices(self) -> None:
        try:
            rA = int(self.rows_A_var.get())
            cA = int(self.cols_A_var.get())
            rB = int(self.rows_B_var.get())
            cB = int(self.cols_B_var.get())
            if min(rA, cA, rB, cB) <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Invalid matrix size")
            return

        for widget in self.frame_A.winfo_children():
            widget.destroy()
        for widget in self.frame_B.winfo_children():
            widget.destroy()

        self.entries_A = []
        self.entries_B = []

        for i in range(rA):
            row: list[ttk.Entry] = []
            for j in range(cA):
                e = ttk.Entry(self.frame_A, width=7, justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                e.insert(0, "0")
                row.append(e)
            self.entries_A.append(row)

        for i in range(rB):
            row = []
            for j in range(cB):
                e = ttk.Entry(self.frame_B, width=7, justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                e.insert(0, "0")
                row.append(e)
            self.entries_B.append(row)

        self.status_var.set(f"A: {rA}x{cA}   B: {rB}x{cB}")
        self._set_result("Matrices created. Enter values and run an operation.")

    def read_matrix(self, entries: list[list[ttk.Entry]]) -> Matrix:
        if not entries:
            raise ValueError("Create matrices first")

        matrix: list[list[float]] = []
        for i, row in enumerate(entries, start=1):
            matrix_row: list[float] = []
            for j, e in enumerate(row, start=1):
                s = e.get().strip()
                if s == "":
                    matrix_row.append(0.0)
                    continue
                try:
                    matrix_row.append(float(s))
                except Exception as ex:
                    raise ValueError(f"Invalid number at ({i}, {j}): '{s}'") from ex
            matrix.append(matrix_row)
        return Matrix(matrix)

    def show_result(self, value) -> None:
        if isinstance(value, Matrix):
            self._set_result(str(value))
        else:
            self._set_result(str(value))

    # Operations
    def add(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            self.show_result(A + B)
            self.status_var.set("Computed A + B")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def subtract(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            self.show_result(A - B)
            self.status_var.set("Computed A - B")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def multiply(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            self.show_result(A * B)
            self.status_var.set("Computed A x B")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def scalar(self) -> None:
        try:
            s = simpledialog.askstring("Scalar", "Enter scalar:")
            if s is None or not str(s).strip():
                raise ValueError("Scalar entry cancelled")
            scalar = float(s)
            A = self.read_matrix(self.entries_A)
            self.show_result(A * scalar)
            self.status_var.set(f"Computed {scalar} x A")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transpose(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self.show_result(A.transpose())
            self.status_var.set("Computed transpose(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def det(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self.show_result(A.determinant())
            self.status_var.set("Computed det(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def inverse(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            inv = A.inverse()
            if inv is None:
                raise ValueError("Matrix is singular (non-invertible)")
            self.show_result(inv)
            self.status_var.set("Computed inv(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def trace(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self.show_result(A.trace())
            self.status_var.set("Computed trace(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rank(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self.show_result(A.rank())
            self.status_var.set("Computed rank(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eigen(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            values, vectors = mo.matrix_eigen(A)
            self._set_result(
                f"Eigenvalues:\n{values}\n\nEigenvectors (columns):\n{vectors}"
            )
            self.status_var.set("Computed eigen(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear(self) -> None:
        for row in self.entries_A:
            for e in row:
                e.delete(0, tk.END)
                e.insert(0, "0")
        for row in self.entries_B:
            for e in row:
                e.delete(0, tk.END)
                e.insert(0, "0")
        self._set_result("Cleared. Blank cells count as 0.")
        self.status_var.set("Cleared")

    def random_A(self) -> None:
        if np is None:
            messagebox.showerror(
                "Error", "Random fill requires numpy (pip install numpy)"
            )
            return
        for row in self.entries_A:
            for e in row:
                e.delete(0, tk.END)
                e.insert(0, str(int(np.random.randint(0, 10))))
        self.status_var.set("Randomized A")


def run_ui() -> None:
    root = tk.Tk()
    MatrixCalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_ui()
