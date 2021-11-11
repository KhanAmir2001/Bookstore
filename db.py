from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)

@app.route('/books')
def books():
    
    con = sqlite3.connect('books.db')
    
    try:
        con.execute('CREATE TABLE books (name TEXT, id INT price FLOAT)')
        print ('Table made')
    except:
        pass
        print("table already created")
        
    con.close()
    
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur.execute("SELECT * from students")
    rows = cur.fetchall();
    
    return render_template("books.html",rows = rows)