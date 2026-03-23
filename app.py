from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            year INTEGER,
            image_url TEXT,
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

@app.route('/library')
def library():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('library.html', books=books)

@app.route('/book/<int:id>')
def book_detail(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('book_detail.html', book=book)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    description = request.form.get('description')
    year = request.form.get('year')
    image_url = request.form.get('image_url')
    
    if title and author:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO books (title, author, description, year, image_url, created_at) VALUES (?, ?, ?, ?, ?, ?)',
            (title, author, description, year, image_url, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()
    return redirect(url_for('library'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('library'))

if __name__ == '__main__':
    app.run(debug=True)