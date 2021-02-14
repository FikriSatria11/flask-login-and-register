from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

app = Flask(__name__)

# mysql://be9e081a4ebcd6:c0b5643f@us-cdbr-east-03.cleardb.com/heroku_a28ba283f0e21b5?reconnect=true

app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'be9e081a4ebcd6'
app.config['MYSQL_PASSWORD'] = 'c0b5643f'
app.config['MYSQL_DB'] = 'heroku_a28ba283f0e21b5'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")

def check_user(iniemail):
    email = iniemail
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from pengguna where email=%s;", (email,))
    user = cur.fetchone()
    cur.close()
    if email == user['email']:
        return True
    else:
        return False

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

if __name__ == '__main__':
    app.secret_key = "inisecretkey2020"
    app.run(debug=True)