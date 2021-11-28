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
from flask import flash, session, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


UPLOAD_FOLDER = 'UPLOAD_FOLDER'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configures upload size for stocks page
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = "secret key" #sets up a secret key and private information to later be used when adding things to basket
sid = 'n0CjmkFtaXI='
pid = 'payment1'
secret = 'TAs9Q2HRNyz8cy8Y186tXFJkq94A'

ALLOWED_EXTNENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) #what type of files can be uploaded

@app.route('/' , methods=['GET', 'POST']) #after the login button is pressed the page is transferred get 
def login():
    if request.method == 'POST':
        return do_the_login(request.form['uname'], request.form['pwd'])
    else:
        return show_the_login_form()

    
def show_the_login_form():
    return render_template('login.html' ,page=url_for('login')) #renders the login page

def do_the_login(u,p):
    con = sqlite3.connect('users.db')
    cur = con.cursor();
    #if u == "admin" and p == "p455w0rd": #shows how admin redirecting would work although not implemented in final version
        # return redirect(url_for('admin'))
    cur.execute("SELECT count(*) FROM users WHERE Username=? AND Password=?;", (u, p)) #checks a database for any username and password on the same row and logs in if true
    
    if(int(cur.fetchone()[0]))>0:
        return redirect(url_for('products'))
    else:
        abort(403)
    
@app.route("/stocks")
def admin():
    #name_of_slider = request.form["name_of_slider"] #slider code that wasnt implemented in final version
    return render_template('stocks.html') #renders page for adding own book to the store as admin

#code taken from https://www.youtube.com/watch?v=I9BBGulrOmo begins here

@app.route("/stocks", methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part') # makes text pop up if file is not uploaded
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #if it passes all checks it is stored in the upload folder so it can be displayed on the website later
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('stocks.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif') # rejecting any of the unwanted file types
        return redirect(request.url)

#code taken from https://www.youtube.com/watch?v=I9BBGulrOmo ends here

#@app.route("/login", methods=['GET'])
#def homepage():
        
    #con = sqlite3.connect("books.db")
    #con.row_factory = sqlite3.Row  #rendered and old version of the page still in files to show previous work
    #cur = con.cursor()
    #cur.execute("SELECT * from books")
    #rows = cur.fetchall();
    
    #return render_template("books.html",books = rows)

@app.route('/add', methods=['POST'])
def add_product_to_cart(): 
    cursor = None
    try:
        _quantity = int(request.form['quantity']) #checks the number for quantity
        _code = request.form['code']
        
        if _quantity and _code and request.method == 'POST':
            con = sqlite3.connect('products.db') #connects to database
            cur = con.cursor();
            cur.execute("SELECT * FROM products WHERE code=?;", [_code]) # finds products based on the code attached
            row = cur.fetchone()
            itemArray = { row[2] : {'name' : row[1], 'code' : row[2], 'quantity' : _quantity, 'price' : row[4], 'image' : row[3], 'total_price': _quantity * row[4]}} # displays the spreadsheet info
            print('itemArray is', itemArray)
            
            all_total_price = 0
            all_total_quantity = 0
            
            session.modified = True
            
            if 'cart_item' in session:
                print('in session')
                if row[2] in session['cart_item']: 
                    for key, value in session['cart_item'].items():
                        if row[2] == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity #handles quantity calculation
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * row[4]
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray) #merges together if multiple added
                    
                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])  #checks cart for values
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price #calculations for both quantity and price
            else:
                session['cart_item'] = itemArray 
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * row[4] # * row 4 as that is price
                
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price 
            
            checksumstr = f"pid={pid:s}&sid={sid:s}&amount={all_total_price:.1f}&token={secret:s}" #uses the secrets in order to encrypt and protect information transferred
            #print('checksumstr is', checksumstr)
            checksum = md5(checksumstr.encode('utf-8')).hexdigest()
            session['checksum'] = checksum
            #print('checksum is', checksum)
            session['sid'] = sid
            session['pid'] = pid
            
            return redirect(url_for('.products'))
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
		
@app.route('/login')
def products():
    try:
        con = sqlite3.connect('products.db')
        cur = con.cursor();
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return render_template('products.html', products=rows) #displays the page making sure the correct amount of items are shown
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()

@app.route('/empty')
def empty_cart():
	try:
		session.clear()
		return redirect(url_for('.products')) #resets page once basket is empty
	except Exception as e:
		print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		for item in session['cart_item'].items():
			if item[0] == code:				
				session['cart_item'].pop(item[0], None)
				if 'cart_item' in session:
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price']) # checks what is currently in the cart
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		
		if all_total_quantity == 0:
			session.clear()
		else:
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		
  
@app.route('/checkout/')    
def checkout():             #checkout was never finished simply redireccts to a blank page upon clicking the button.
    print("hello world")
    return("hi")
    con = sqlite3.connect('products.db')
    cur = con.cursor();
    cur.execute("SELECT price FROM products") # would have obtained price from products and added together
    rows = cur.fetchall()
    return render_template('products.html', products=rows)
    cur.close()
    con.close()


    
    
app.run(host="0.0.0.0")