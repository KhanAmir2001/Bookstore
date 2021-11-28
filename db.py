from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)

@app.route('/books')
def books():
    con = sqlite3.connect('books.db')
    
    try:
        con.execute('CREATE TABLE books (name TEXT, isbn INT, price DOUBLE, date TEXT, desc TEXT, cover TEXT, quantity INT)')
        
        print ('Table made')
    except:
        pass
        print("table already created")
        
    con.close()
    
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('INSERT INTO books(isbn, name, cover, desc, price, date, quantity) VALUES (0, "little red riding hood", "red.jpg", "girl fights wold", 12.00, "16/03/67", 4)')
    cur.execute("SELECT * from books")
    rows = cur.fetchall();
    
    return render_template("test.html",rows = rows)

app.run(host="0.0.0.0")