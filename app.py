from flask import Flask,request,render_template,jsonify
import sqlite3
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d


def init_sqlite_db():
    conn = sqlite3.connect('e-commerce.db')
    print("opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS register(name TEXT,email TEXT,password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS products(image TEXT,title TEXT,price INTEGER,description TEXT)')
    print("Table created successfully")
    conn.close()

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
        return jsonify(msg)
        con.close()


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

#inserting into table products
@app.route('/shop-products/')
def add_products():
    try:
        with sqlite3.connect('e-commerce.db') as con:
            # con.row_factory = dict_factory
            cur=con.cursor()
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/HxRVdJZX/project24.jpg', 'Stuck on you', 'R529.99', 'Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/Sx14wBtz/project10.jpg','Life is a concert and Im a lead sing','R750.00','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/RVR4T67d/project11.jpg','Growing up was never easy','R312.89','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price, description ) VALUES ('https://i.postimg.cc/MGcwx9h3/project9.jpg','Through the years','R999.99','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/nc0fm8xw/project1.jpg','Too cute to handle','R499.95','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/mZ9r7gpp/project18.jpg','I cant break these chains that I hold','R625.70','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/RZZ9pSGB/project7.jpg','She is never afraid','R450.00','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/HxXC8VWQ/project8.jpg','Own your crown','R629.99','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/CKWgKj0h/project4.jpg','Lost in the moments','R301.99','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/nrqcx3Qf/project19.jpg','Its okay to be scared','R500.49','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/hPgKxbdh/project13.jpg','Angry Youth','R865.00','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/kgG3FjXM/project5.jpg','There is one memory of us','R1000.50','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/W1TtNcnW/project23.jpg','My life My story','R700.00','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/qM8zHv86/project20.jpg','Delightful Memories','R1200.99','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            cur.execute("INSERT INTO products(image,title,price ,description ) VALUES ('https://i.postimg.cc/ncth2f6F/project22.jpg','Im addicted to','R835.00','Lorem ipsum dolor sit amet consectetur adipiscing elit.')")
            con.commit()
            msg = "records added successfully."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)

    finally:
        con.close()
        return jsonify(msg)

@app.route('/show-products/', methods=["GET"])
def show_products():
    data = []
    try:
        with sqlite3.connect('e-commerce.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            data = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database." + str(e))
    finally:
        con.close()
        return jsonify(data)




















# @app.route('/send-email/', methods=["POST", "GET"])
# def send_email():
#
#     try:
#         # subject = request.form['subject']
#         name = request.form['name']
#         email = request.form['email']
#         message = MIMEText(request.form['message'])
#         # message['Subject'] = subject
#         message['From'] = email
#         message['To'] = email
#
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         sender_email = email
#         receiver_email = "dotwanazenande@gmail.com"
#         password = "07307865"
#
#         server.starttls()
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message.as_string())
#         server.quit()
#     except smtplib.SMTPException as e:
#         return "Something wrong happened: " + e
#     return render_template('contact.html')
#

if __name__=='__main__':
    app.run(debug=True)

