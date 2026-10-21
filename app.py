"""
Student Management System — Flask Application
A simple web application to manage student records using Firebase Firestore.
"""

import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from firebase_config import initialize_firebase

# Load environment variables from .env file
load_dotenv()

# ── Flask App Setup ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-to-a-random-secret-key")

# Enable CSRF protection
csrf = CSRFProtect(app)

# ── Firebase Initialization ──────────────────────────────────────────────────
db, firebase_error = initialize_firebase()


# ── Helper Functions ─────────────────────────────────────────────────────────

def is_valid_email(email):
    """Check if the email address has a valid format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_all_students():
    """Fetch all student documents from Firestore and return as a list."""
    students_ref = db.collection("students")
    docs = students_ref.stream()
    students = []
    for doc in docs:
        student = doc.to_dict()
        student["student_id"] = doc.id
        students.append(student)
    return students


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """Dashboard page showing total students and quick links."""
    if firebase_error:
        flash(firebase_error, "danger")
        return render_template("dashboard.html", total_students=0)

    try:
        students = get_all_students()
        total_students = len(students)
    except Exception as e:
        flash(f"Error fetching data from Firebase: {str(e)}", "danger")
        total_students = 0

    return render_template("dashboard.html", total_students=total_students)


@app.route("/students")
def view_students():
    """Display all students with optional search functionality."""
    if firebase_error:
        flash(firebase_error, "danger")
        return render_template("students.html", students=[], search_query="")

    search_query = request.args.get("search", "").strip()

    try:
        students = get_all_students()

        # Filter students if a search query is provided
        if search_query:
            query_lower = search_query.lower()
            students = [
                s for s in students
                if query_lower in s.get("student_id", "").lower()
                or query_lower in s.get("full_name", "").lower()
            ]
    except Exception as e:
        flash(f"Error fetching students: {str(e)}", "danger")
        students = []

    return render_template(
        "students.html", students=students, search_query=search_query
    )


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    """Show the add-student form (GET) or save a new student (POST)."""
    if firebase_error:
        flash(firebase_error, "danger")
        return render_template("add_student.html")

    if request.method == "POST":
        # Collect form data
        student_id = request.form.get("student_id", "").strip()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        academic_year = request.form.get("academic_year", "").strip()

        # ── Validation ───────────────────────────────────────────────────
        errors = []
        if not student_id:
            errors.append("Student ID is required.")
        if not full_name:
            errors.append("Full Name is required.")
        if not email:
            errors.append("Email Address is required.")
        elif not is_valid_email(email):
            errors.append("Please enter a valid email address.")
        if not department:
            errors.append("Department is required.")
        if not academic_year:
            errors.append("Academic Year is required.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("add_student.html")

        # Check for duplicate Student ID
        try:
            doc = db.collection("students").document(student_id).get()
            if doc.exists:
                flash("A student with this ID already exists.", "danger")
                return render_template("add_student.html")
        except Exception as e:
            flash(f"Error checking student ID: {str(e)}", "danger")
            return render_template("add_student.html")

        # Save to Firestore
        try:
            db.collection("students").document(student_id).set({
                "full_name": full_name,
                "email": email,
                "department": department,
                "academic_year": academic_year,
            })
            flash("Student added successfully!", "success")
            return redirect(url_for("view_students"))
        except Exception as e:
            flash(f"Error saving student: {str(e)}", "danger")
            return render_template("add_student.html")

    # GET request — show empty form
    return render_template("add_student.html")


@app.route("/students/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    """Show the edit form (GET) or update a student record (POST)."""
    if firebase_error:
        flash(firebase_error, "danger")
        return redirect(url_for("view_students"))

    # Fetch the existing student
    try:
        doc = db.collection("students").document(student_id).get()
        if not doc.exists:
            flash("Student not found.", "warning")
            return redirect(url_for("view_students"))
        student = doc.to_dict()
        student["student_id"] = doc.id
    except Exception as e:
        flash(f"Error fetching student: {str(e)}", "danger")
        return redirect(url_for("view_students"))

    if request.method == "POST":
        # Collect form data
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        academic_year = request.form.get("academic_year", "").strip()

        # ── Validation ───────────────────────────────────────────────────
        errors = []
        if not full_name:
            errors.append("Full Name is required.")
        if not email:
            errors.append("Email Address is required.")
        elif not is_valid_email(email):
            errors.append("Please enter a valid email address.")
        if not department:
            errors.append("Department is required.")
        if not academic_year:
            errors.append("Academic Year is required.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("edit_student.html", student=student)

        # Update Firestore
        try:
            db.collection("students").document(student_id).update({
                "full_name": full_name,
                "email": email,
                "department": department,
                "academic_year": academic_year,
            })
            flash("Student updated successfully!", "success")
            return redirect(url_for("view_students"))
        except Exception as e:
            flash(f"Error updating student: {str(e)}", "danger")
            return render_template("edit_student.html", student=student)

    # GET request — show form with existing data
    return render_template("edit_student.html", student=student)


@app.route("/students/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    """Delete a student record from Firestore."""
    if firebase_error:
        flash(firebase_error, "danger")
        return redirect(url_for("view_students"))

    try:
        doc = db.collection("students").document(student_id).get()
        if not doc.exists:
            flash("Student not found.", "warning")
            return redirect(url_for("view_students"))

        db.collection("students").document(student_id).delete()
        flash("Student deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting student: {str(e)}", "danger")

    return redirect(url_for("view_students"))


# ── Run the Application ─────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
