from flask import Flask 
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import make_response
import urllib.request
import os
from werkzeug.utils import secure_filename
import sqlite3

UPLOAD_FOLDER = 'UPLOAD_FOLDER'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTNENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
    #name_of_slider = request.form["name_of_slider"]
    return render_template('stocks.html')

@app.route("/stocks", methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('stocks.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

#https://www.youtube.com/watch?v=I9BBGulrOmo

@app.route("/", methods=['GET'])
def homepage():
        
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

@app.route("/", methods=['POST'])
def buttons():
    if request.method == 'POST':
        if request.form['Log_Out'] == 'Log_Out':
            return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['Add_Stocks'] == 'Add_Stocks':
            return redirect(url_for('admin'))
        



    
    
app.run(host="0.0.0.0")