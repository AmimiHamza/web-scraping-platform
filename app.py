from flask import Flask, request, render_template, send_from_directory, send_file,redirect, url_for, flash, session
from scrjobs import scrapejobs
from scrproducts import scrapeproducts
from scrproduct import scrapeproduct
from scrcomments import scrapecomments
from scrmovie import scrapemovie
from scrallmovies import scrapeallmovies
from full import scrapecrypto
from delta import generate_delta_file
from datetime import datetime
import re
import os
import pandas as pd
import shutil
import sqlite3
import hashlib
from functools import wraps


def hash_password(password):
    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    hashed_password = hasher.hexdigest()
    return hashed_password





app = Flask(__name__)
app.secret_key = 'robotmza'
# Configuration for SQLite database
DATABASE = 'datab.db'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged' not in session or not session['logged']:
            flash('You need to log in to access this page.', 'error')
            return redirect(url_for('formlogin'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET'])
def fakeindex():
    if 'logged' not in session or not session['logged']:
        return render_template('fakeindex.html')
    else:
        return render_template('index.html')



    

@app.route('/form')
def form():
    return render_template('signup.html')

@app.route('/formlogin')
def formlogin():
    return render_template('login.html',data='')



@app.route('/<path:filename>')
def serve_non_html(filename):    
    if not filename.endswith('.html'):
        return send_from_directory('static', filename)
    else:
        if('logged' in session and session['logged']):
            return send_from_directory('static', filename)
        else:
            return redirect(url_for('formlogin'))




        
    



        

@app.route('/download/<path:file_path>')
@login_required
def download_file(file_path):
    return send_file(f"{file_path}.txt",as_attachment=True)

@app.route('/downloadxlsx/<path:file_path>')
@login_required
def download_xlsx_file(file_path):
    return send_file(f"{file_path}.xlsx",as_attachment=True)




@app.route('/printjobs', methods=['GET'])
@login_required
def print_variable_jobs():
    skill = request.args.get('variable')
    scrapejobs(skill)
    # Read data from text file
    with open(f"jobs/{skill}.txt", "r") as file:
        lines = file.readlines()
    return render_template('printjobs.html', skill=skill, lines=lines)



@app.route('/printproducts', methods=['GET'])
@login_required
def print_variable_products():
    product = request.args.get('variable')
    scrapeproducts(product)
    # Read data from text file
    with open('products/' + product + '.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return render_template('printproducts.html', product=product, lines=lines)

@app.route('/printproduct', methods=['GET'])
@login_required
def print_variable_product():
    url = request.args.get('variable')
    scrapeproduct(url)
    surl = re.sub(r'[^a-zA-Z0-9.-]', '_', url)   
    # Read data from text file
    with open(f"products/{surl}.txt", "r") as file:
        lines = file.readlines()
    return render_template('printproduct.html', product=surl, lines=lines)

@app.route('/printcomments', methods=['GET'])
def print_variable_comments():
    url = request.args.get('variable')
    scrapecomments(url)
    surl = re.sub(r'[^a-zA-Z0-9.-]', '_', url)   
    # Read data from text file
    with open(f"video_comments/{surl}.txt", "r") as file:
        lines = file.readlines()
    return render_template('printcomments.html', product=surl, lines=lines)

@app.route('/printmovie', methods=['GET'])
@login_required
def print_movie():
    movie_name = request.args.get('variable')
    scrapemovie(movie_name)
    # Read data from text file
    with open(f"movies/{movie_name}.txt", "r") as file:
        lines = file.readlines()
    return render_template('printmovie.html', product=movie_name, lines=lines)

@app.route('/printallmovies', methods=['GET'])
@login_required
def print_allmovies():
    genre= request.args.get('variable')
    scrapeallmovies(genre)
    # Read data from text file
    with open(f"movies/{genre}.txt", "r") as file:
        lines = file.readlines()
    return render_template('printallmovies.html', product=genre, lines=lines)

@app.route('/printcrypto', methods=['GET'])
@login_required
def print_crypto():
    print('hello')
    scrapecrypto(3)
    file_path = "crypto/cryptosn.xlsx"
    df = pd.read_excel(file_path)

    # Convert the DataFrame to a list of lists for rendering in the template
    data = df.values.tolist()
    current_datetime = datetime.now()
    return render_template('printcrypto.html', data=data,current_datetime=current_datetime)

@app.route('/diff')
@login_required
def diff():
    generate_delta_file()
    file_path = "crypto/delta.xlsx"
    df = pd.read_excel(file_path)

    # Convert the DataFrame to a list of lists for rendering in the template
    data = df.values.tolist()
    os.remove("crypto/cryptos.xlsx")

    # Rename CRYPTOSN.xlsx to CRYPTOS.xlsx
    os.rename("crypto/cryptosn.xlsx", "crypto/cryptos.xlsx")
    return render_template('printcryptodelta.html', data=data)

@app.route('/exitm')
@login_required
def exitm1():
    shutil.rmtree("movies")
    os.mkdir("movies")
    return send_from_directory('static', 'platforms.html')

@app.route('/exitm1')
def exitm():
    shutil.rmtree("movies")
    os.mkdir("movies")
    return send_from_directory('static', 'platforms.html')

@app.route('/exitp')
@login_required
def exitp():
    shutil.rmtree("products")
    os.mkdir("products")
    return send_from_directory('static', 'platforms.html')

@app.route('/exitj')
@login_required
def exitj():
    shutil.rmtree("jobs")
    os.mkdir("jobs")
    return send_from_directory('static', 'platforms.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    fname = request.form['fname']
    email = request.form['email']
    password = request.form['password']
    password = hash_password(password)
    birthday = request.form['birthday']

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        # Check if the email already exists in the database
        cur.execute('SELECT email FROM users WHERE email = ?', (email,))
        existing_email = cur.fetchone()

        if existing_email:
            flash('Email already exists. Please use a different email.', 'error')
            return  render_template('signup.html',data='oups!!, it seems like your Email is already used, please try again')
        cur.execute('CREATE TABLE IF NOT EXISTS users (name TEXT,fname TEXT,email TEXT,password TEXT, birthday DATE)')
        cur.execute('INSERT INTO users (name, fname, email, password, birthday) VALUES (?, ?, ?, ?, ?)',
                    (name, fname, email, password, birthday))
        con.commit()

    return redirect(url_for('fakeindex'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password = hash_password(password)

        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute('SELECT name FROM users WHERE email = ?', (email,))
            name = cur.fetchone()
            cur.execute('SELECT password FROM users WHERE email = ?', (email,))
            result = cur.fetchone()

            if result and result[0] == password:
                # Password matches, user is authenticated
                # You can set a session variable or perform any other authentication tasks here
                session['logged'] = True

                flash('Login successful!', 'success')
                #i should creat a file
                return redirect(url_for('fakeindex'))
            else:
                return render_template('login.html', data='Invalid email or password. Please try again.')
                flash('Invalid email or password. Please try again.', 'error')
                #return redirect(url_for('formlogin'))
    else:
        # If the request method is GET, it means the user is just accessing the login page
        # You can render the login form template here
        return render_template('login.html', data='')

@app.route('/logout')
def logout():
    # Clear the 'logged' key from the session when the user logs out
    session.pop('logged', None)
    return redirect(url_for('fakeindex'))

if __name__ == '__main__':
    app.run()