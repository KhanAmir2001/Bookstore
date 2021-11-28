from flask import Flask
from flask import render_template
import sqlite3 

con = sqlite3.connect('products.db')

con.execute('CREATE TABLE products(isbn INT unsigned, name VARCHAR(255), code VARCHAR(255), image TEXT, price DOUBLE)') #creates database with settings

con.close()  
con = sqlite3.connect('products.db')

con.execute('INSERT INTO products(isbn, name, code, image, price) VALUES (1, "Little red riding hood", "AMTR01", "product-images/red.jpg", 14.00),(2, "Alice in wonderland", "USB02", "product-images/alice.jpg", 32.00),(3, "Cinderella", "SH03", "product-images/cind.jpg", 1.00),(4, "minecraft survival guide", "LPN4", "product-images/mine.jpg", 80000.00);')
            #,(5, "FinePix Pro2 3D Camera", "3DCAM01", "product-images/camera.jpg", 150000.00),(6, "Simple Mobile", "MB06", "product-images/mobile.jpg", 3000.00),(7, "Luxury Ultra thin Wrist Watch", "WristWear03", "product-images/watch.jpg", 3000.00),(8, "Headphones", "HD08", "product-images/headphone.jpg", 400.00);')
            # inserts all the relevant data into the database
con.commit()
con.close()  