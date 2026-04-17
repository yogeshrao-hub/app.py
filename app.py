from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# (Same HTML as your code — no change needed)
HOME_HTML = """PASTE YOUR SAME HTML HERE"""
EXPENSES_HTML = """PASTE YOUR SAME HTML HERE"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/get_expenses')
def get_expenses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    data = [{"id": r[0], "name": r[1], "amount": r[2]} for r in c.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (data['name'], data['amount']))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/expenses')
def expenses_page():
    return render_template_string(EXPENSES_HTML)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
