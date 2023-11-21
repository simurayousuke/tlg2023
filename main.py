from flask import Flask, render_template, jsonify
import webbrowser
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products"
    cursor.execute(query)
    rows = cursor.fetchall()

    data_array = []
    for row in rows:
        data_array.append(list(row))

    cursor.close()
    conn.close()

    return render_template('index.html', title="2023", data=data_array)

@app.route('/data')
def data():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    app.run(debug=False, port=80, threaded=True)