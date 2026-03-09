# ui.py

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import numpy as np
import matrix_operations as mo


class MatrixCalculatorUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")

        self.entries_A = []
        self.entries_B = []

        self.build_dimension_controls()
        self.build_matrix_frames()
        self.build_buttons()
        self.build_result_area()

    # ---------------------------
    # Dimension Controls
    # ---------------------------

    def build_dimension_controls(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Rows A").grid(row=0, column=0)
        tk.Label(frame, text="Cols A").grid(row=0, column=1)

        self.rows_A = tk.Entry(frame, width=5)
        self.cols_A = tk.Entry(frame, width=5)

        self.rows_A.grid(row=1, column=0)
        self.cols_A.grid(row=1, column=1)

        tk.Label(frame, text="Rows B").grid(row=0, column=2)
        tk.Label(frame, text="Cols B").grid(row=0, column=3)

        self.rows_B = tk.Entry(frame, width=5)
        self.cols_B = tk.Entry(frame, width=5)

        self.rows_B.grid(row=1, column=2)
        self.cols_B.grid(row=1, column=3)

        tk.Button(frame, text="Create Matrices",
                  command=self.create_matrices).grid(row=1, column=4, padx=10)

    # ---------------------------
    # Matrix Frames
    # ---------------------------

    def build_matrix_frames(self):

        container = tk.Frame(self.root)
        container.pack()

        self.frame_A = tk.LabelFrame(container, text="Matrix A")
        self.frame_A.pack(side=tk.LEFT, padx=10)

        self.frame_B = tk.LabelFrame(container, text="Matrix B")
        self.frame_B.pack(side=tk.LEFT, padx=10)

    # ---------------------------
    # Buttons
    # ---------------------------

    def build_buttons(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="A + B",
                  command=self.add).grid(row=0, column=0)

        tk.Button(frame, text="A - B",
                  command=self.subtract).grid(row=0, column=1)

        tk.Button(frame, text="A × B",
                  command=self.multiply).grid(row=0, column=2)

        tk.Button(frame, text="Scalar × A",
                  command=self.scalar).grid(row=0, column=3)

        tk.Button(frame, text="Transpose A",
                  command=self.transpose).grid(row=1, column=0)

        tk.Button(frame, text="Determinant A",
                  command=self.det).grid(row=1, column=1)

        tk.Button(frame, text="Inverse A",
                  command=self.inverse).grid(row=1, column=2)

        tk.Button(frame, text="Trace A",
                  command=self.trace).grid(row=1, column=3)

        tk.Button(frame, text="Rank A",
                  command=self.rank).grid(row=2, column=0)

        tk.Button(frame, text="Eigen A",
                  command=self.eigen).grid(row=2, column=1)

        tk.Button(frame, text="Random A",
                  command=self.random_A).grid(row=2, column=2)

        tk.Button(frame, text="Clear",
                  command=self.clear).grid(row=2, column=3)

    # ---------------------------
    # Result Area
    # ---------------------------

    def build_result_area(self):

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Result").pack()

        self.result = tk.Text(frame, height=10, width=60)
        self.result.pack()

    # ---------------------------
    # Matrix Creation
    # ---------------------------

    def create_matrices(self):

        try:
            rA = int(self.rows_A.get())
            cA = int(self.cols_A.get())
            rB = int(self.rows_B.get())
            cB = int(self.cols_B.get())
        except:
            messagebox.showerror("Error", "Invalid matrix size")
            return

        for widget in self.frame_A.winfo_children():
            widget.destroy()

        for widget in self.frame_B.winfo_children():
            widget.destroy()

        self.entries_A = []
        self.entries_B = []

        for i in range(rA):
            row = []
            for j in range(cA):
                e = tk.Entry(self.frame_A, width=5)
                e.grid(row=i, column=j)
                row.append(e)
            self.entries_A.append(row)

        for i in range(rB):
            row = []
            for j in range(cB):
                e = tk.Entry(self.frame_B, width=5)
                e.grid(row=i, column=j)
                row.append(e)
            self.entries_B.append(row)

    # ---------------------------
    # Helpers
    # ---------------------------

    def read_matrix(self, entries):

        matrix = []
        for row in entries:
            matrix_row = []
            for e in row:
                matrix_row.append(float(e.get()))
            matrix.append(matrix_row)
        return matrix

    def show_result(self, value):

        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, str(value))

    # ---------------------------
    # Operations
    # ---------------------------

    def add(self):
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            res = mo.add_matrices(A, B)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def subtract(self):
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            res = mo.subtract_matrices(A, B)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def multiply(self):
        try:
            A = self.read_matrix(self.entries_A)
            B = self.read_matrix(self.entries_B)
            res = mo.multiply_matrices(A, B)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def scalar(self):
        try:
            scalar = float(simpledialog.askstring("Scalar", "Enter scalar:"))
            A = self.read_matrix(self.entries_A)
            res = mo.scalar_multiply(A, scalar)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transpose(self):
        try:
            A = self.read_matrix(self.entries_A)
            res = mo.transpose_matrix(A)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def det(self):
        try:
            A = self.read_matrix(self.entries_A)
            res = mo.determinant_matrix(A)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def inverse(self):
        try:
            A = self.read_matrix(self.entries_A)
            res = mo.inverse_matrix(A)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def trace(self):
        try:
            A = self.read_matrix(self.entries_A)
            res = mo.trace_matrix(A)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rank(self):
        try:
            A = self.read_matrix(self.entries_A)
            res = mo.rank_matrix(A)
            self.show_result(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eigen(self):
        try:
            A = self.read_matrix(self.entries_A)
            values, vectors = mo.eigen_values_vectors(A)
            self.show_result(f"Eigenvalues:\n{values}\n\nEigenvectors:\n{vectors}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------
    # Extra Features
    # ---------------------------

    def clear(self):
        for row in self.entries_A:
            for e in row:
                e.delete(0, tk.END)

        for row in self.entries_B:
            for e in row:
                e.delete(0, tk.END)

        self.result.delete(1.0, tk.END)

    def random_A(self):
        try:
            for row in self.entries_A:
                for e in row:
                    e.delete(0, tk.END)
                    e.insert(0, np.random.randint(0, 10))
        except:
            pass