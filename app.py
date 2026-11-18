from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import threading
import os
import shutil
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return render_template('index.html', selected_date=selected_date, no_data=True)
    
    return render_template('index.html', selected_date=selected_date, attendance_data=attendance_data)


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'
    chrome_paths = [
        shutil.which('chrome'),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    chrome = next((path for path in chrome_paths if path and os.path.isfile(path)), None)

    if chrome:
        threading.Timer(1, lambda: subprocess.Popen([chrome, url])).start()
    else:
        print("Chrome was not found. Add chrome.exe to PATH or install Chrome.")

    app.run(debug=True, use_reloader=False)
