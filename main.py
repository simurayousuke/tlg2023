from flask import Flask, render_template
import webbrowser
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
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

if __name__ == "__main__":
    app.run(debug=True, port=8080, threaded=True)