from datetime import date, datetime
import os
import sqlite3
import subprocess
import sys
import threading
import webbrowser

from flask import Flask, jsonify, redirect, render_template, request, url_for


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "attendance.db")
app = Flask(__name__)

task_lock = threading.Lock()
task_state = {"status": "idle", "name": "", "message": "", "error": ""}


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    conn = get_connection()
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS attendance "
            "(name TEXT, time TEXT, date DATE, UNIQUE(name, date))"
        )
        conn.commit()
    finally:
        conn.close()


def run_script(script_name):
    return subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, script_name)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


def run_task(task_name):
    try:
        if task_name == "register":
            capture = run_script("get_faces_from_camera_tkinter.py")
            if capture.returncode != 0:
                raise RuntimeError(capture.stderr.strip() or "The face registration window closed with an error.")

            extraction = run_script("features_extraction_to_csv.py")
            if extraction.returncode != 0:
                raise RuntimeError(extraction.stderr.strip() or "Could not update the face recognition data.")
            message = "Registration finished and face data was updated. You can register another student or take attendance."
        else:
            attendance = run_script("attendance_taker.py")
            if attendance.returncode != 0:
                raise RuntimeError(attendance.stderr.strip() or "The attendance camera closed with an error.")
            message = "Attendance session finished. Present students are listed below."

        with task_lock:
            task_state.update(status="done", message=message, error="")
    except Exception as exc:
        with task_lock:
            task_state.update(status="error", message="The operation could not be completed.", error=str(exc)[-1500:])


def start_task(task_name):
    with task_lock:
        if task_state["status"] == "running":
            return False
        task_state.update(status="running", name=task_name, message="Starting…", error="")
        threading.Thread(target=run_task, args=(task_name,), daemon=True).start()
        return True


@app.route("/")
def index():
    selected_date = request.args.get("date") or date.today().isoformat()
    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date().isoformat()
    except ValueError:
        selected_date = date.today().isoformat()

    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT name, time FROM attendance WHERE date = ? ORDER BY time, name",
            (selected_date,),
        ).fetchall()
    finally:
        conn.close()

    with task_lock:
        current_task = dict(task_state)
    return render_template(
        "index.html",
        selected_date=selected_date,
        attendance_data=rows,
        task=current_task,
    )


@app.post("/register")
def register():
    start_task("register")
    return redirect(url_for("index"))


@app.post("/take-attendance")
def take_attendance():
    start_task("attendance")
    return redirect(url_for("index"))


@app.get("/task-status")
def task_status():
    with task_lock:
        return jsonify(task_state)


if __name__ == "__main__":
    initialize_database()
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False, use_reloader=False)
