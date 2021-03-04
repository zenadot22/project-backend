from flask import Flask,request,render_template,jsonify
import sqlite3
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('e-commerce.db')
    print("opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS register(name TEXT,email TEXT,password TEXT)')
    print("Table created successfully")
    conn.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


init_sqlite_db()

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/register/',methods=['POST'])
def add_user():
    msg = None
    try:
        post_data = request.get_json()
        name = post_data['name']
        email = post_data['email']
        password = post_data['password']

        with sqlite3.connect('e-commerce.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO register(name, email, password ) VALUES (?,?,?)",
                        (name, email, password))
            con.commit()
            msg = "records added successfully."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)

    finally:
        con.close()
        return jsonify(msg)

@app.route('/show-items/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('e-commerce.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM register")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)


if __name__=='__main__':
    app.run(debug=True)

