from flask import Flask, render_template, jsonify, request
import webbrowser
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html', title="2023")

@app.route('/table')
def table():
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

    return render_template('table.html', title="table", data=data_array)

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html', title="2023")

@app.route('/chat', methods=['POST'])
def comment():
    comment = request.json.get('comment')
    if comment is None:
        return "Please provide a 'comment' query parameter.", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO chat (comment) VALUES (?)"
    cursor.execute(query, (comment,))
        
    conn.commit()
    conn.close()

    return jsonify({'result': 'success', 'message': "Comment success."})

@app.route('/comments')
def comments():
    latest = request.args.get('latest', type=int)
    if latest is None:
        latest = 0
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT comment FROM chat WHERE id > ?"
    cursor.execute(query, (latest,))
    rows = cursor.fetchall()

    query_latest = "SELECT MAX(id) AS max_id FROM chat"
    cursor.execute(query_latest)
    latest_result = cursor.fetchone()

    conn.close()

    return jsonify({"latest":latest_result['max_id'] if latest_result and latest_result['max_id'] is not None else 0,"data":[row[0] for row in rows]})


@app.route('/data')
def data():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products"
    cursor.execute(query)
    rows = cursor.fetchall()

    query_latest = "SELECT MAX(id) AS max_id FROM history"
    cursor.execute(query_latest)
    latest_result = cursor.fetchone()

    conn.close()

    latest = latest_result['max_id'] if latest_result and latest_result['max_id'] is not None else 0
    return jsonify({"latest":latest, "data":[dict(row) for row in rows]})

@app.route('/diff')
def diff():
    latest = request.args.get('latest', type=int)
    if latest is None:
        latest = 0
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM history WHERE id > ?"
    cursor.execute(query, (latest,))
    rows = cursor.fetchall()

    query_latest = "SELECT MAX(id) AS max_id FROM history"
    cursor.execute(query_latest)
    latest_result = cursor.fetchone()

    conn.close()

    return jsonify({"latest":latest_result['max_id'] if latest_result and latest_result['max_id'] is not None else 0,"data":[dict(row) for row in rows]})

@app.route('/update')
def update():
    id = request.args.get('id', type=int)
    if id is None:
        return "Please provide a 'id' query parameter.", 400
    amount = request.args.get('amount', type=int)
    if amount is None:
        return "Please provide a 'amount' query parameter.", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE products SET amount = ? WHERE id = ?"
        cursor.execute(query, (amount, id))

        if cursor.rowcount == 0:
            return jsonify({'result': 'fail', 'message': "No record found with the provided id."}), 404

        history_query = "INSERT INTO history (target, amount) VALUES (?, ?)"
        cursor.execute(history_query, (id, amount))
        
        conn.commit()

        return jsonify({'result': 'success', 'message': "Update success."})

    except Exception as e:
        return jsonify({'result': 'fail', 'message': str(e)}), 500

    finally:
        conn.close()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    # app.run(debug=False, port=8080, threaded=True)
