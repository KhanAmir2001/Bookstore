from flask import Flask 
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import make_response
import sqlite3

app = Flask(__name__)

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login(request.form['uname'], request.form['pwd'])
    else:
        return show_the_login_form()

    
def show_the_login_form():
    return render_template('login.html' ,page=url_for('login'))

def do_the_login(u,p):
    con = sqlite3.connect('users.db')
    cur = con.cursor();
    #if u == "admin" and p == "p455w0rd":
        # return redirect(url_for('admin'))
    cur.execute("SELECT count(*) FROM users WHERE Username=? AND Password=?;", (u, p))
    
    if(int(cur.fetchone()[0]))>0:
        return redirect(url_for('homepage'))
    else:
        abort(403)
    
@app.route("/stocks")
def admin():
    return render_template('stocks.html')

@app.route("/", methods=['GET'])
def homepage():
        
    if request.method == 'GET':
        print("hello")
    con = sqlite3.connect('books.db')
    
    try:
        con.execute('CREATE TABLE books (name TEXT, id INT, price FLOAT)')
        
        print ('Table made')
    except:
        pass
        print("table already created")
        
    con.close()
    
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from books")
    rows = cur.fetchall();
    
    return render_template("books.html",rows = rows)


    
    
app.run(host="0.0.0.0")