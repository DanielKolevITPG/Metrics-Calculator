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
from collections.abc import Callable
from typing import Optional

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

            # Error highlight for invalid cells
            style.configure("Error.TEntry", fieldbackground="#ffe8e8")
        except Exception:
            pass

        self._ui_font = ("Segoe UI", 10)
        self._mono_font = ("Consolas", 10)
        self.root.option_add("*Font", self._ui_font)

        self.entries_A: list[list[ttk.Entry]] = []
        self.entries_B: list[list[ttk.Entry]] = []

        self._last_output_matrix: Optional[Matrix] = None
        # Use Callable here for type checkers; runtime type is a no-arg callback.
        self._last_operation: Optional[tuple[str, Callable[[], None]]] = None

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

        self.root.bind_all("<Control-Shift-V>", lambda _e: self.paste_A())
        self.root.bind_all("<Control-Alt-V>", lambda _e: self.paste_B())
        self.root.bind_all("<Control-Shift-C>", lambda _e: self.copy_output())
        self.root.bind_all("<F5>", lambda _e: self.rerun_last())

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

        ttk.Separator(frame, orient="horizontal").grid(
            row=1, column=0, columnspan=12, sticky="ew", pady=(10, 8)
        )

        ttk.Button(frame, text="Paste A", command=self.paste_A).grid(
            row=2, column=0, columnspan=2, sticky="w"
        )
        ttk.Button(frame, text="Paste B", command=self.paste_B).grid(
            row=2, column=2, columnspan=2, sticky="w", padx=(6, 0)
        )
        ttk.Button(frame, text="Copy A", command=self.copy_A).grid(
            row=2, column=4, columnspan=2, sticky="w", padx=(16, 0)
        )
        ttk.Button(frame, text="Copy B", command=self.copy_B).grid(
            row=2, column=6, columnspan=2, sticky="w", padx=(6, 0)
        )
        ttk.Button(frame, text="Swap A/B", command=self.swap_AB).grid(
            row=2, column=8, columnspan=2, sticky="w", padx=(16, 0)
        )
        ttk.Button(frame, text="Copy Output", command=self.copy_output).grid(
            row=2, column=10, columnspan=2, sticky="w", padx=(6, 0)
        )

        hint = ttk.Label(
            frame,
            text="Shortcuts: Ctrl+Shift+V Paste A, Ctrl+Alt+V Paste B, Ctrl+Shift+C Copy Output, F5 Re-run",
            foreground="#444444",
        )
        hint.grid(row=3, column=0, columnspan=12, sticky="w", pady=(8, 0))

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

        # "Quick Compute" lets users pick an operation and hit Enter.
        quick = ttk.Frame(frame)
        quick.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 8))
        quick.columnconfigure(1, weight=1)

        ttk.Label(quick, text="Quick Compute").grid(row=0, column=0, sticky="w")
        self.quick_var = tk.StringVar(value="A + B")
        self.quick_combo = ttk.Combobox(
            quick,
            textvariable=self.quick_var,
            values=[
                "A + B",
                "A - B",
                "A x B",
                "Scalar x A",
                "Transpose A",
                "Determinant A",
                "Inverse A",
                "Trace A",
                "Rank A",
                "Eigen A",
            ],
            state="readonly",
        )
        self.quick_combo.grid(row=0, column=1, sticky="ew", padx=(8, 8))
        self.quick_run_btn = ttk.Button(quick, text="Run", command=self.run_quick)
        self.quick_run_btn.grid(row=0, column=2, sticky="e")

        quick_hint = ttk.Label(
            quick,
            text="Tip: press Enter on any cell to move; F5 re-runs last operation.",
            foreground="#444444",
        )
        quick_hint.grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 0))

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
                row=r + 1, column=c, padx=4, pady=4, sticky="ew"
            )

        for c in range(4):
            frame.columnconfigure(c, weight=1)

        # Small workflow helpers
        helper = ttk.Frame(frame)
        helper.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(8, 0))
        ttk.Button(helper, text="Output -> A", command=self._move_output_to_A).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(helper, text="Output -> B", command=self._move_output_to_B).pack(
            side="left"
        )

        # Enter in combobox runs quick op
        self.quick_combo.bind("<Return>", lambda _e: self.run_quick())

    def run_quick(self) -> None:
        op = self.quick_var.get().strip()
        mapping = {
            "A + B": self.add,
            "A - B": self.subtract,
            "A x B": self.multiply,
            "Scalar x A": self.scalar,
            "Transpose A": self.transpose,
            "Determinant A": self.det,
            "Inverse A": self.inverse,
            "Trace A": self.trace,
            "Rank A": self.rank,
            "Eigen A": self.eigen,
        }
        fn = mapping.get(op)
        if fn is None:
            self.status_var.set("Unknown operation")
            return
        fn()

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
                self._setup_entry(e, "A", i, j)
                row.append(e)
            self.entries_A.append(row)

        for i in range(rB):
            row = []
            for j in range(cB):
                e = ttk.Entry(self.frame_B, width=7, justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                e.insert(0, "0")
                self._setup_entry(e, "B", i, j)
                row.append(e)
            self.entries_B.append(row)

        self.status_var.set(f"A: {rA}x{cA}   B: {rB}x{cB}")
        self._set_result("Matrices created. Enter values and run an operation.")

        # Focus the first cell for quicker data entry
        if self.entries_A and self.entries_A[0] and self.entries_A[0][0]:
            self.entries_A[0][0].focus_set()
            self.entries_A[0][0].selection_range(0, tk.END)

    def read_matrix(self, entries: list[list[ttk.Entry]]) -> Matrix:
        if not entries:
            raise ValueError("Create matrices first")

        # Clear any previous error styles
        for row in entries:
            for e in row:
                try:
                    e.configure(style="TEntry")
                except Exception:
                    pass

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
                    try:
                        e.configure(style="Error.TEntry")
                        e.focus_set()
                        e.selection_range(0, tk.END)
                    except Exception:
                        pass
                    raise ValueError(f"Invalid number at ({i}, {j}): '{s}'") from ex
            matrix.append(matrix_row)
        return Matrix(matrix)

    def show_result(self, value) -> None:
        if isinstance(value, Matrix):
            self._last_output_matrix = value
            self._set_result(str(value))
        else:
            self._last_output_matrix = None
            self._set_result(str(value))

    def _remember_op(self, label: str, fn: Callable[[], None]) -> None:
        self._last_operation = (label, fn)

    def rerun_last(self) -> None:
        if not self._last_operation:
            self.status_var.set("No previous operation")
            return
        label, fn = self._last_operation
        try:
            fn()
            self.status_var.set(f"Re-ran: {label}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Clipboard helpers
    def _copy_to_clipboard(self, text: str) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update_idletasks()

    def _format_entries_as_text(self, entries: list[list[ttk.Entry]]) -> str:
        # Tab-separated rows; friendly for spreadsheets.
        rows: list[str] = []
        for row in entries:
            parts: list[str] = []
            for e in row:
                s = e.get().strip()
                parts.append(s if s != "" else "0")
            rows.append("\t".join(parts))
        return "\n".join(rows)

    def _parse_matrix_text(self, text: str) -> list[list[float]]:
        s = text.strip()
        if not s:
            raise ValueError("Clipboard is empty")

        # Accept either ';' separated rows or newline-separated rows.
        if ";" in s:
            row_chunks = [r.strip() for r in s.split(";")]
        else:
            row_chunks = [r.strip() for r in s.splitlines()]

        rows: list[list[float]] = []
        for r in row_chunks:
            if not r:
                continue
            # Accept tabs, commas, or spaces.
            r = r.replace(",", " ")
            parts = [p for p in r.replace("\t", " ").split(" ") if p != ""]
            if not parts:
                continue
            row: list[float] = []
            for p in parts:
                row.append(float(p))
            rows.append(row)

        if not rows:
            raise ValueError("No numbers found in clipboard")

        cols = len(rows[0])
        for idx, row in enumerate(rows, start=1):
            if len(row) != cols:
                raise ValueError(
                    f"Inconsistent row length at row {idx}: expected {cols}, got {len(row)}"
                )

        return rows

    def _fill_entries(
        self, entries: list[list[ttk.Entry]], data: list[list[float]]
    ) -> None:
        for i, row in enumerate(entries):
            for j, e in enumerate(row):
                e.delete(0, tk.END)
                e.insert(0, str(data[i][j]))

    def paste_A(self) -> None:
        try:
            text = self.root.clipboard_get()
        except Exception:
            messagebox.showerror("Error", "Clipboard is not available")
            return

        try:
            data = self._parse_matrix_text(text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.rows_A_var.set(len(data))
        self.cols_A_var.set(len(data[0]))
        self.create_matrices()
        self._fill_entries(self.entries_A, data)
        self.status_var.set("Pasted matrix into A")

    def paste_B(self) -> None:
        try:
            text = self.root.clipboard_get()
        except Exception:
            messagebox.showerror("Error", "Clipboard is not available")
            return

        try:
            data = self._parse_matrix_text(text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.rows_B_var.set(len(data))
        self.cols_B_var.set(len(data[0]))
        self.create_matrices()
        self._fill_entries(self.entries_B, data)
        self.status_var.set("Pasted matrix into B")

    def copy_A(self) -> None:
        self._copy_to_clipboard(self._format_entries_as_text(self.entries_A))
        self.status_var.set("Copied A to clipboard")

    def copy_B(self) -> None:
        self._copy_to_clipboard(self._format_entries_as_text(self.entries_B))
        self.status_var.set("Copied B to clipboard")

    def copy_output(self) -> None:
        text = self.result.get(1.0, tk.END).strip()
        if not text:
            self.status_var.set("Nothing to copy")
            return
        self._copy_to_clipboard(text)
        self.status_var.set("Copied output")

    def swap_AB(self) -> None:
        A = self.read_matrix(self.entries_A)
        B = self.read_matrix(self.entries_B)

        self.rows_A_var.set(A.rows)
        self.cols_A_var.set(A.cols)
        self.rows_B_var.set(B.rows)
        self.cols_B_var.set(B.cols)
        self.create_matrices()

        self._fill_entries(self.entries_A, [[float(x) for x in row] for row in B.data])
        self._fill_entries(self.entries_B, [[float(x) for x in row] for row in A.data])
        self.status_var.set("Swapped A and B")

    # Entry behavior
    def _setup_entry(self, entry: ttk.Entry, which: str, i: int, j: int) -> None:
        entry.bind(
            "<FocusIn>",
            lambda _e, ent=entry: (ent.selection_range(0, tk.END), None),
        )
        entry.bind(
            "<Return>",
            lambda e, w=which, r=i, c=j: self._on_enter(e, w, r, c, forward=True),
        )
        entry.bind(
            "<Shift-Return>",
            lambda e, w=which, r=i, c=j: self._on_enter(e, w, r, c, forward=False),
        )
        entry.bind(
            "<Up>",
            lambda e, w=which, r=i, c=j: self._move_focus(e, w, r - 1, c),
        )
        entry.bind(
            "<Down>",
            lambda e, w=which, r=i, c=j: self._move_focus(e, w, r + 1, c),
        )
        entry.bind(
            "<Left>",
            lambda e, w=which, r=i, c=j: self._move_focus(e, w, r, c - 1),
        )
        entry.bind(
            "<Right>",
            lambda e, w=which, r=i, c=j: self._move_focus(e, w, r, c + 1),
        )

    def _grid_for(self, which: str) -> list[list[ttk.Entry]]:
        return self.entries_A if which == "A" else self.entries_B

    def _move_focus(self, event, which: str, r: int, c: int):
        grid = self._grid_for(which)
        if not grid:
            return "break"

        r = max(0, min(r, len(grid) - 1))
        c = max(0, min(c, len(grid[0]) - 1))
        grid[r][c].focus_set()
        grid[r][c].selection_range(0, tk.END)
        return "break"

    def _on_enter(self, event, which: str, r: int, c: int, forward: bool):
        grid = self._grid_for(which)
        if not grid:
            return "break"

        rows = len(grid)
        cols = len(grid[0])
        idx = r * cols + c
        idx = idx + (1 if forward else -1)
        idx = max(0, min(idx, rows * cols - 1))
        nr, nc = divmod(idx, cols)
        grid[nr][nc].focus_set()
        grid[nr][nc].selection_range(0, tk.END)
        return "break"

    def _move_output_to_A(self) -> None:
        if self._last_output_matrix is None:
            messagebox.showerror("Error", "Last output is not a matrix")
            return

        m = self._last_output_matrix
        self.rows_A_var.set(m.rows)
        self.cols_A_var.set(m.cols)
        self.create_matrices()
        self._fill_entries(self.entries_A, [[float(x) for x in row] for row in m.data])
        self.status_var.set("Moved output -> A")

    def _move_output_to_B(self) -> None:
        if self._last_output_matrix is None:
            messagebox.showerror("Error", "Last output is not a matrix")
            return

        m = self._last_output_matrix
        self.rows_B_var.set(m.rows)
        self.cols_B_var.set(m.cols)
        self.create_matrices()
        self._fill_entries(self.entries_B, [[float(x) for x in row] for row in m.data])
        self.status_var.set("Moved output -> B")

    # Operations
    def add(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            self._remember_op("A + B", self.add)
            self.show_result(A + B)
            self.status_var.set("Computed A + B")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def subtract(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            self._remember_op("A - B", self.subtract)
            self.show_result(A - B)
            self.status_var.set("Computed A - B")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def multiply(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            self._remember_op("A x B", self.multiply)
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
            self._remember_op("Scalar x A", self.scalar)
            self.show_result(A * scalar)
            self.status_var.set(f"Computed {scalar} x A")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transpose(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self._remember_op("Transpose A", self.transpose)
            self.show_result(A.transpose())
            self.status_var.set("Computed transpose(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def det(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self._remember_op("Determinant A", self.det)
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
            self._remember_op("Inverse A", self.inverse)
            self.show_result(inv)
            self.status_var.set("Computed inv(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def trace(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self._remember_op("Trace A", self.trace)
            self.show_result(A.trace())
            self.status_var.set("Computed trace(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rank(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            self._remember_op("Rank A", self.rank)
            self.show_result(A.rank())
            self.status_var.set("Computed rank(A)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eigen(self) -> None:
        try:
            A = self.read_matrix(self.entries_A)
            values, vectors = mo.matrix_eigen(A)
            self._remember_op("Eigen A", self.eigen)
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
