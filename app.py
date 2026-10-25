from pathlib import Path
import re
import sqlite3
import os
import secrets
from contextlib import contextmanager

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            class_name TEXT NOT NULL,
            marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100),
            contact TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")


def validate_form(data):
    name = data.get("name", "").strip()
    roll_no = data.get("roll_no", "").strip()
    class_name = data.get("class_name", "").strip()
    contact = data.get("contact", "").strip()
    marks_text = data.get("marks", "").strip()
    errors = []
    if not name or len(name) > 80:
        errors.append("Enter a name (up to 80 characters).")
    if not roll_no or len(roll_no) > 30:
        errors.append("Enter a roll number (up to 30 characters).")
    if not class_name or len(class_name) > 50:
        errors.append("Enter a class (up to 50 characters).")
    if not re.fullmatch(r"[+0-9()\-\s]{7,20}", contact):
        errors.append("Enter a valid contact number (7–20 digits or phone symbols).")
    try:
        marks = float(marks_text)
        if not 0 <= marks <= 100:
            errors.append("Marks must be between 0 and 100.")
    except ValueError:
        marks = None
        errors.append("Enter marks as a number between 0 and 100.")
    return {"name": name, "roll_no": roll_no, "class_name": class_name,
            "marks": marks, "contact": contact}, errors


@app.get("/")
def index():
    query = request.args.get("q", "").strip()
    with get_db() as conn:
        if query:
            like = f"%{query}%"
            students = conn.execute("""SELECT * FROM students
                WHERE name LIKE ? OR roll_no LIKE ? OR class_name LIKE ?
                ORDER BY id DESC""", (like, like, like)).fetchall()
        else:
            students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
        total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        average = conn.execute("SELECT AVG(marks) FROM students").fetchone()[0]
    return render_template("index.html", students=students, query=query,
                           total=total, average=round(average or 0, 1))


@app.route("/students/new", methods=["GET", "POST"])
def create_student():
    if request.method == "POST":
        student, errors = validate_form(request.form)
        if not errors:
            try:
                with get_db() as conn:
                    conn.execute("""INSERT INTO students
                        (name, roll_no, class_name, marks, contact)
                        VALUES (:name, :roll_no, :class_name, :marks, :contact)""", student)
                flash("Student added successfully.", "success")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                errors.append("That roll number already exists. Use a unique roll number.")
        for error in errors:
            flash(error, "error")
        return render_template("form.html", student=student, page_title="Add student")
    return render_template("form.html", student={}, page_title="Add student")


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db() as conn:
        existing = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if existing is None:
        flash("Student record not found.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        student, errors = validate_form(request.form)
        if not errors:
            try:
                with get_db() as conn:
                    conn.execute("""UPDATE students SET name=:name, roll_no=:roll_no,
                        class_name=:class_name, marks=:marks, contact=:contact WHERE id=:id""",
                        {**student, "id": student_id})
                flash("Student record updated.", "success")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                errors.append("That roll number belongs to another student.")
        for error in errors:
            flash(error, "error")
        return render_template("form.html", student=student, page_title="Edit student")
    return render_template("form.html", student=dict(existing), page_title="Edit student")


@app.post("/students/<int:student_id>/delete")
def delete_student(student_id):
    with get_db() as conn:
        cur = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cur.rowcount:
        flash("Student record deleted.", "success")
    else:
        flash("Student record not found.", "error")
    return redirect(url_for("index"))


@app.get("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(debug=True)
