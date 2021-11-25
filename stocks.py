from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)

@app.route("/stocks")

def createpage():
    return render_template('stocks.html' )

app.run(host="0.0.0.0")