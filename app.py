# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)

# events = []

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         new_event = {
#             'title': request.form.get('title'),
#             'date': request.form.get('date'),
#             'time': request.form.get('time'),
#             'priority': request.form.get('priority')
#         }
#         if new_event['title']:
#             events.append(new_event)
            
#         return redirect(url_for('index'))
    
#     return render_template('index.html', events=events)

# @app.route('/delete/<int:event_id>')
# def delete_event(event_id):
#     if 0 <= event_id < len(events):
#         events.pop(event_id)
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('tasks.db'):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                priority TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        task = request.form.get('task')
        date = request.form.get('date')
        time = request.form.get('time')
        priority = request.form.get('priority')
        if task:
            conn.execute('INSERT INTO events (task, date, time, priority) VALUES (?, ?, ?, ?)', (task, date, time, priority))
            conn.commit()
        conn.close()
        return redirect(url_for('index'))
    tasks = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)