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
    cur.execute("SELECT count(*) FROM users WHERE name=? AND pwd=?;", (u, p))
    if(int(cur.fetchone()[0]))>0:
        return f'<H1>Success!</H1>'
    else:
        abort(403)
    
app.run(host="0.0.0.0")