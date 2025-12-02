"""
GeoTutor ITS – Fully adaptive, multi‑user area tutor with:
- Ontology-based expert model (optional, via GeoTutor.owl)
- Bayesian Knowledge Tracing mastery model
- Randomised problems (easy/medium/hard)
- Multi‑user login and persistent profiles
"""

import json
import os
import random
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import owlready2
from owlready2 import get_ontology

try:
    from owlready2 import sync_reasoner
except ImportError:
    sync_reasoner = None


STUDENTS_FILE = "students_data.json"
ONTO_PATH = "GeoTutor.owl"


def load_students() -> dict:
    if os.path.exists(STUDENTS_FILE):
        try:
            with open(STUDENTS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Corrupt file; start fresh but keep a backup
            os.rename(STUDENTS_FILE, f"{STUDENTS_FILE}.bak_{datetime.now().timestamp()}")
    return {}


def save_students(db: dict) -> None:
    with open(STUDENTS_FILE, "w") as f:
        json.dump(db, f, indent=2)


def load_ontology():
    """Load ontology if available; never crash if missing or Java not configured."""
    if not os.path.exists(ONTO_PATH):
        print("Warning: GeoTutor.owl not found. Ontology features disabled.")
        return None

    onto = get_ontology(ONTO_PATH).load()
    print("Ontology loaded successfully.")

    if sync_reasoner is not None:
        try:
            with onto:
                sync_reasoner(infer_property_values=True, infer_data_property_values=True)
            print("Reasoner completed.")
        except Exception as e:
            print("Reasoner warning:", e)
    else:
        print("Reasoner not available (sync_reasoner not imported).")

    return onto


STUDENTS_DB = load_students()
ONTOLOGY = load_ontology()


def generate_problem(shape: str, difficulty: str) -> dict:
    """Random problem generator for unlimited practice."""
    if difficulty == "easy":
        if shape == "Triangle":
            b = random.randint(3, 8)
            h = random.randint(3, 8)
            return {"base": b, "height": h, "area": round(0.5 * b * h, 2)}
        if shape == "Square":
            s = random.randint(3, 8)
            return {"side": s, "area": float(s * s)}
        # Rectangle
        l = random.randint(4, 8)
        w = random.randint(3, 6)
        return {"length": l, "width": w, "area": float(l * w)}

    if difficulty == "medium":
        if shape == "Triangle":
            b = random.randint(6, 12)
            h = random.uniform(5, 10)
            return {"base": b, "height": round(h, 1), "area": round(0.5 * b * h, 2)}
        if shape == "Square":
            s = random.randint(7, 15)
            return {"side": s, "area": float(s * s)}
        l = random.randint(8, 15)
        w = random.randint(5, 10)
        return {"length": l, "width": w, "area": float(l * w)}

    # hard
    if shape == "Triangle":
        b = random.uniform(8.0, 20.0)
        h = random.uniform(6.0, 15.0)
        return {"base": round(b, 1), "height": round(h, 1), "area": round(0.5 * b * h, 2)}
    if shape == "Square":
        s = random.uniform(10.0, 25.0)
        return {"side": round(s, 1), "area": round(s * s, 2)}
    l = random.uniform(10.0, 30.0)
    w = random.uniform(5.0, 15.0)
    return {"length": round(l, 1), "width": round(w, 1), "area": round(l * w, 2)}


class BKT:
    """Bayesian Knowledge Tracing student model."""

    def __init__(self, initial: float = 0.1):
        self.p_known = float(initial)
        self.p_guess = 0.2
        self.p_slip = 0.1
        self.p_learn = 0.3

    def update(self, correct: bool) -> float:
        if correct:
            num = self.p_known * (1 - self.p_slip)
            den = num + (1 - self.p_known) * self.p_guess
        else:
            num = self.p_known * self.p_slip
            den = num + (1 - self.p_known) * (1 - self.p_guess)

        if den != 0:
            self.p_known = num / den

        self.p_known += (1 - self.p_known) * self.p_learn
        return round(self.p_known, 3)


class GeoTutorApp:
    def __init__(self, root: tk.Tk, student_id: str):
        self.root = root
        self.student_id = student_id
        self.root.title(f"GeoTutor ITS – Welcome, {student_id}!")
        self.root.geometry("1250x820")
        self.root.configure(bg="#f8f9fa")

        if student_id not in STUDENTS_DB:
            STUDENTS_DB[student_id] = {
                "mastery": 0.1,
                "difficulty": "easy",
                "attempts": 0,
                "correct": 0,
                "last_login": datetime.now().isoformat(timespec="seconds"),
            }
        self.profile = STUDENTS_DB[student_id]
        self.bkt = BKT(self.profile.get("mastery", 0.1))

        self.difficulty = self.profile.get("difficulty", "easy")
        self.shape_var = tk.StringVar(value="Triangle")
        self.current_problem: dict | None = None

        self._build_ui()
        self._new_problem()

    def _save_profile(self, correct: bool) -> None:
        self.profile["mastery"] = float(self.bkt.p_known)
        self.profile["difficulty"] = self.difficulty
        self.profile["attempts"] = self.profile.get("attempts", 0) + 1
        if correct:
            self.profile["correct"] = self.profile.get("correct", 0) + 1
        self.profile["last_login"] = datetime.now().isoformat(timespec="seconds")
        save_students(STUDENTS_DB)

    def _new_problem(self) -> None:
        shape = self.shape_var.get()
        self.current_problem = generate_problem(shape, self.difficulty)
        self._update_inputs()

        self.feedback.delete("1.0", "end")
        self.feedback.insert(
            "end",
            f"New problem generated!\n"
            f"Shape: {shape}\n"
            f"Difficulty: {self.difficulty.capitalize()}\n"
            "Use the formula and enter the area.",
        )
        self._draw_shape()
        self._update_mastery_bar()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg="#2c3e50", pady=15)
        header.pack(fill="x")
        tk.Label(
            header,
            text=f"GeoTutor ITS – Student: {self.student_id}",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2c3e50",
        ).pack()

        main = tk.Frame(self.root, bg="#f8f9fa")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Left – problem statement
        left = tk.LabelFrame(main, text=" Problem ", font=("Arial", 14, "bold"), bg="#e3f2fd")
        left.pack(side="left", fill="y", padx=10)

        ttk.Label(left, text="Shape:").pack(pady=5)
        shape_box = ttk.Combobox(
            left,
            textvariable=self.shape_var,
            values=["Triangle", "Square", "Rectangle"],
            state="readonly",
        )
        shape_box.pack(pady=5)
        self.shape_var.trace_add("write", lambda *_: self._new_problem())

        self.input_frame = tk.Frame(left, bg="#e3f2fd")
        self.input_frame.pack(pady=15, fill="x")

        ttk.Button(left, text="Show Example", command=self._show_example).pack(pady=5)
        ttk.Button(left, text="New Problem", command=self._new_problem).pack(pady=5)

        # Center – answer + feedback
        center = tk.Frame(main, bg="white", relief="sunken", bd=2)
        center.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center, text="Your Area Answer:", font=("Arial", 18)).pack(pady=10)
        self.answer_entry = tk.Entry(center, font=("Arial", 16), width=15, justify="center")
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<Return>", lambda _e: self._check_answer())

        self.feedback = tk.Text(center, height=12, font=("Arial", 12), bg="#f0f8ff", wrap="word")
        self.feedback.pack(pady=10, fill="both", expand=True)

        ttk.Button(center, text="Check Answer", command=self._check_answer).pack(pady=10)

        # Right – visualisation + mastery
        right = tk.Frame(main, bg="#f0fdf4")
        right.pack(side="right", fill="y", padx=10)

        tk.Label(right, text="Shape Preview", font=("Arial", 14, "bold"), bg="#f0fdf4").pack(pady=10)
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, right)
        self.canvas.get_tk_widget().pack()

        self.mastery_label = tk.Label(
            right,
            text=f"Mastery: {int(self.bkt.p_known * 100)}%",
            font=("Arial", 16, "bold"),
            bg="#f0fdf4",
        )
        self.mastery_label.pack(pady=20)

        self.mastery_bar = ttk.Progressbar(right, length=350, maximum=100, value=self.bkt.p_known * 100)
        self.mastery_bar.pack(pady=10)

    def _update_inputs(self) -> None:
        for w in self.input_frame.winfo_children():
            w.destroy()
        prob = self.current_problem
        shape = self.shape_var.get()

        if shape == "Triangle":
            tk.Label(self.input_frame, text=f"Base = {prob['base']}", bg="#e3f2fd", font=("Arial", 12)).pack(pady=4)
            tk.Label(self.input_frame, text=f"Height = {prob['height']}", bg="#e3f2fd", font=("Arial", 12)).pack(
                pady=4
            )
        elif shape == "Square":
            tk.Label(self.input_frame, text=f"Side = {prob['side']}", bg="#e3f2fd", font=("Arial", 12)).pack(pady=4)
        else:
            tk.Label(self.input_frame, text=f"Length = {prob['length']}", bg="#e3f2fd", font=("Arial", 12)).pack(
                pady=4
            )
            tk.Label(self.input_frame, text=f"Width = {prob['width']}", bg="#e3f2fd", font=("Arial", 12)).pack(
                pady=4
            )

        self.answer_entry.delete(0, "end")

    def _draw_shape(self) -> None:
        self.ax.clear()
        p = self.current_problem
        shape = self.shape_var.get()

        if shape == "Triangle":
            self.ax.fill(
                [0, p["base"], p["base"] / 2, 0],
                [0, 0, p["height"], 0],
                "#8b5cf6",
                alpha=0.8,
            )
        elif shape == "Square":
            s = p["side"]
            self.ax.fill([0, s, s, 0, 0], [0, 0, s, s, 0], "#f59e0b", alpha=0.8)
        else:
            l, w = p["length"], p["width"]
            self.ax.fill([0, l, l, 0, 0], [0, 0, w, w, 0], "#10b981", alpha=0.8)

        self.ax.axis("equal")
        self.ax.axis("off")
        self.canvas.draw()

    def _show_example(self) -> None:
        shape = self.shape_var.get()
        ex = generate_problem(shape, "easy")

        if shape == "Triangle":
            msg = (
                f"Triangle Example:\nBase = {ex['base']}, Height = {ex['height']}\n"
                f"Area = ½ × base × height = {ex['area']}"
            )
        elif shape == "Square":
            msg = f"Square Example:\nSide = {ex['side']}\nArea = side × side = {ex['area']}"
        else:
            msg = (
                f"Rectangle Example:\nLength = {ex['length']}, Width = {ex['width']}\n"
                f"Area = length × width = {ex['area']}"
            )

        messagebox.showinfo("Worked Example", msg)

    def _check_answer(self) -> None:
        if not self.current_problem:
            return

        try:
            user = float(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a number for the area.")
            return

        correct_area = float(self.current_problem["area"])
        correct = abs(user - correct_area) < 0.1

        self.bkt.update(correct)

        self.feedback.insert(
            "end",
            f"\nYour answer: {user:.2f}   |   Correct: {correct_area:.2f}\n"
        )

        if correct:
            self.feedback.insert("end", "CORRECT! Well done!\n")
            if self.difficulty == "easy":
                self.difficulty = "medium"
            elif self.difficulty == "medium":
                self.difficulty = "hard"
        else:
            self.feedback.insert(
                "end",
                "Incorrect. Remember to apply the correct area formula.\n"
            )
            if self.difficulty == "hard":
                self.difficulty = "medium"
            elif self.difficulty == "medium":
                self.difficulty = "easy"

        self._save_profile(correct)
        self._update_mastery_bar()
        self._new_problem()

    def _update_mastery_bar(self) -> None:
        pct = int(self.bkt.p_known * 100)
        self.mastery_bar["value"] = pct
        self.mastery_label.config(text=f"Mastery: {pct}%")


def login() -> str:
    # Minimal root just for the dialog
    root = tk.Tk()
    root.withdraw()
    student = simpledialog.askstring("Login", "Enter your Student ID (e.g., 202300123):")
    root.destroy()

    if not student:
        raise SystemExit
    return student.strip()


if __name__ == "__main__":
    student_id = login()
    main_root = tk.Tk()
    app = GeoTutorApp(main_root, student_id)
    main_root.mainloop()