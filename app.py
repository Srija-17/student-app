from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----------------------
# DATABASE INITIALIZATION
# ----------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            reg_no TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            semester TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------
# ROUTES
# ----------------------
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        reg_no = request.form["reg_no"]
        email = request.form["email"]
        course = request.form["course"]
        semester = request.form["semester"]

        # Save to DB
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO students (name, reg_no, email, course, semester)
            VALUES (?, ?, ?, ?, ?)
        """, (name, reg_no, email, course, semester))
        conn.commit()
        conn.close()

        return redirect("/success")

    return render_template("register.html")

@app.route("/success")
def success():
    return "<h2>Student Registered Successfully ✅</h2>"

if __name__ == "__main__":
    app.run(debug=True)
