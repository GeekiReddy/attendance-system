from flask import Flask, render_template, request
import sqlite3
from datetime import date

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template("index.html")


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template('register.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Email or Password"

    return render_template('login.html')


# Attendance Route
@app.route('/attendance', methods=['POST'])
def attendance():

    today = str(date.today())

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM attendance WHERE date=?",
        (today,)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "Attendance Already Marked Today!"

    cursor.execute(
        "INSERT INTO attendance(date,status) VALUES(?,?)",
        (today, "Present")
    )

    conn.commit()
    conn.close()

    return "Attendance Marked Successfully!"
@app.route('/history')
def history():

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attendance")

    records = cursor.fetchall()

    conn.close()

    return render_template("history.html", records=records)
@app.route('/logout')
def logout():
    return render_template('login.html')    
@app.route('/test')
def test():
    return "Flask is working"
@app.route('/admin')
def admin():

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attendance")

    records = cursor.fetchall()

    conn.close()

    return render_template("admin.html", records=records)

if __name__ == '__main__':
    app.run(debug=True)