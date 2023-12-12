from flask import Flask, render_template, jsonify, request
import webbrowser
import sqlite3
import random
import requests

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_data_array():
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

    return data_array


def is_all_shown():
    conn = get_db_connection()
    cursor = conn.cursor()

    ret = False

    query = "SELECT * FROM products where isShow=0"
    cursor.execute(query)

    if cursor.fetchone() is None:
        ret = True

    cursor.close()
    conn.close()

    return ret


def get_rank_str(rank):
    if rank == 4:
        return "UR"
    if rank == 3:
        return "SR"
    if rank == 2:
        return "SP"
    if rank == 1:
        return "R"
    return "Unknown"


def get_amount_by_id(id):
    ret = 0
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT amount FROM products WHERE id = ?"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    if result is not None:
        ret = result['amount']

    conn.close()

    return ret


@app.route('/')
def index():
    return render_template('index.html', title="2023")


@app.route('/table')
def table():
    return render_template('table.html', title="table", data=get_data_array(), allShown=is_all_shown())


@app.route('/92c7264931784fbc9d82cd9f7d5faae4')
def edit():
    data_array = get_data_array()
    return render_template('edit.html', title="edit", data=data_array, data_size=len(data_array))


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

    return jsonify({"latest": latest_result['max_id'] if latest_result and latest_result['max_id'] is not None else 0,
                    "data": [row[0] for row in rows]})


@app.route('/latestchatid')
def latestChatId():
    conn = get_db_connection()
    cursor = conn.cursor()

    query_latest = "SELECT MAX(id) AS max_id FROM chat"
    cursor.execute(query_latest)
    latest_result = cursor.fetchone()

    conn.close()

    return str(latest_result['max_id'] if latest_result and latest_result['max_id'] is not None else 0)


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
    return jsonify({"latest": latest, "data": [dict(row) for row in rows]})


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

    return jsonify({"latest": latest_result['max_id'] if latest_result and latest_result['max_id'] is not None else 0,
                    "data": [dict(row) for row in rows]})


@app.route('/3a26e808a4114092842e131456a1ec00')
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


@app.route('/9c1473fbc1c041e7999d3874ce36a9bf')
def set_show():
    id = request.args.get('id', type=int)
    if id is None:
        return "Please provide a 'id' query parameter.", 400
    show = request.args.get('show', type=int)
    if show is None:
        return "Please provide a 'show' query parameter.", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE products SET isShow = ? WHERE id = ?"
        cursor.execute(query, (show, id))

        if cursor.rowcount == 0:
            return jsonify({'result': 'fail', 'message': "No record found with the provided id."}), 404

        history_query = "INSERT INTO history (target, amount) VALUES (?, ?)"
        cursor.execute(history_query, (id, get_amount_by_id(id)))

        conn.commit()

        return jsonify({'result': 'success', 'message': "Update success."})

    except Exception as e:
        return jsonify({'result': 'fail', 'message': str(e)}), 500

    finally:
        conn.close()


@app.route('/gacha')
def gacha():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT rank, SUM(amount) FROM products group by rank"
    cursor.execute(query)
    rows = cursor.fetchall()

    data_array = []
    for row in rows:
        value = 0
        if row[0] == 4:
            value = 1
        elif row[0] == 3:
            value = 2
        elif row[0] == 2 or row[0] == 1:
            value = 3
        for _ in range(row[1]):
            data_array.append(value)

    cursor.close()
    conn.close()

    random.shuffle(data_array)

    # Print the total amount of 1, 2, 3 in data_array
    total_one = data_array.count(1)
    total_two = data_array.count(2)
    total_three = data_array.count(3)
    print([total_one, total_two, total_three])

    return render_template('gacha.html', title="gacha", data=data_array)


@app.route('/fdc97e7318264f11bdf16825e2de7ff9')
def stuff():
    return render_template('stuff.html', title="stuff", data=get_data_array())


@app.route('/4f897ded2b844565915fee965dc45370')
def sub():
    id = request.args.get('id', type=int)
    if id is None:
        return "Please provide a 'id' query parameter.", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query_amount = "SELECT id,rank,name,amount FROM products WHERE id = ?"
        cursor.execute(query_amount, (id,))
        amount_result = cursor.fetchone()
        amount = amount_result['amount'] if amount_result and amount_result['amount'] is not None else 0

        if amount <= 0:
            return jsonify({'result': 'fail', 'message': "No record found or amount <= 0."}), 400

        query = "UPDATE products SET amount = amount - 1 WHERE id = ?"
        cursor.execute(query, (id,))

        history_query = "INSERT INTO history (target, amount) VALUES (?, ?)"
        cursor.execute(history_query, (id, amount))

        conn.commit()

        slack_url = "https://hooks.slack.com/triggers/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"
        payload = {
            "name": amount_result['name'],
            "id": amount_result['id'],
            "rank": get_rank_str(amount_result['rank']),
            "amount": amount - 1
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(slack_url, json=payload, headers=headers)

        return jsonify({'result': 'success', 'message': "Update success."})

    except Exception as e:
        return jsonify({'result': 'fail', 'message': str(e)}), 500

    finally:
        conn.close()


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
    # app.run(debug=False, port=8080, threaded=True)
