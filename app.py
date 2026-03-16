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
from datetime import datetime

app = Flask(__name__)

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/planner')
def planner():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('planner.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)',
            (title, description, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()
    return redirect(url_for('planner'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('planner'))

if __name__ == '__main__':
    app.run(debug=True)