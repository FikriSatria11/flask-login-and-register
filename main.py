from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
# import mysql.connector

app = Flask(__name__)
mysql = MySQL()
# mysql://be9e081a4ebcd6:c0b5643f@us-cdbr-east-03.cleardb.com/heroku_a28ba283f0e21b5?reconnect=true


# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# # app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'latihan_flask'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# heroku
# mysql://be9e081a4ebcd6:c0b5643f@us-cdbr-east-03.cleardb.com/heroku_a28ba283f0e21b5?reconnect=true
app.config['DATABASE_URL'] = 'mysql://be9e081a4ebcd6:c0b5643f@us-cdbr-east-03.cleardb.com/heroku_a28ba283f0e21b5?reconnect=true'
app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'be9e081a4ebcd6'
app.config['MYSQL_PASSWORD'] = 'c0b5643f'
app.config['MYSQL_DB'] = 'heroku_a28ba283f0e21b5'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'inisecretkey2020'

# mysql://bf4433c4e8d563:eb3288bd@us-cdbr-east-03.cleardb.com/heroku_0d58f5e5eb33d90?reconnect=true
# app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
# app.config['MYSQL_USER'] = 'bf4433c4e8d563'
# app.config['MYSQL_PASSWORD'] = 'eb3288bd'
# app.config['MYSQL_DB'] = 'heroku_0d58f5e5eb33d90'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

def check_user(iniemail):
    email = iniemail
    # print(email)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from pengguna where email=%s;", (email,))
    user = cur.fetchone()
    cur.close()
    # print(user)
    # print(type(user))
    if user == None:
        # print("false")
        return False
    else:
        # print("true")
        return True

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", keterangan="input data")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        checkuser = check_user(email)
        
        if checkuser:
            return render_template("register.html", keterangan="email sudah ada")

        cur = mysql.connection.cursor()
        cur.execute("insert into pengguna (name, email, password) values (%s,%s,%s);", (name,email,hash_password))
        mysql.connection.commit()
        cur.close()
        session['name'] = name
        session['email'] = email
        return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    keterangan = "input email and password"
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select * from pengguna where email=%s;", (email,))
        user = cur.fetchone()
        cur.close()

        print(user)
        print(type(user))

        if user:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return render_template("login.html", keterangan="Error password or user not match 1")
        else:
            return render_template("login.html", keterangan="Error password or user not match 2")
    else:
        return render_template("login.html", keterangan=keterangan)

@app.route("/logout")
def logout():
    session.clear()
    return render_template('home.html')

@app.route("/test", methods=["GET", "POST"])
def test():
    cur = mysql.connection.cursor()
    cur.execute("select * from pengguna ;")
    user = cur.fetchone()
    cur.close()

    return render_template('test.html', data=user)

if __name__ == '__main__':
    # app.secret_key = "inisecretkey2020"
    app.run(debug=True)