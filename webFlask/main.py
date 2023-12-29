import os
import sqlite3

from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Importing from a sibling directory
import sys
sys.path.append(".")  # Add parent directory to the Python path
from src.dbConnection import create_connection, create_table, add, showDB, clearDB

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies).
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False #session timeout after browser is closed
#app.config['PERMANENT_SESSION_LIFETIME'] = 300 #session timeout in seconds
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def main_page():
    return render_template('/layout.html')

#connect to database
db_conn = sqlite3.connect('finance.db', check_same_thread=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #check if username is empty
        if username == '':
            return apology("must provide username", 403)
        elif username == '':
            return apology("must provide password", 403)
        
        # check if username exists
        user = db_conn.execute("SELECT * FROM USERS WHERE username = ?", (username,))
        # take the first row of the result
        user = user.fetchone()
        
        if user is None:
            return apology("invalid username", 403)
        elif user[2] != password:
            return apology("invalid password", 403)
        elif user[2] == password:
            # Remember which user has logged in.
            session["user_id"] = user[0]
            # Redirect to dashboard
            return dashboard()
    else:    
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return render_template("logout.html")

@app.route("/dashboard")
@login_required
def dashboard():
    current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    # Identify the current user.
    if session.get("user_id") == 'None':
        session.clear()
        return redirect("/")
    else:
        user_id = session["user_id"]
        print("dashboard user_id: ", user_id)
        #identify current user_name
        user = db_conn.execute("SELECT * FROM USERS WHERE id = ?", (session["user_id"],))
        user = user.fetchone()
           
           
        # Create a list of stock's information
        stock_info_list = []
        # Initialize variales here for correct scope
        symbol = ''
        name = ''
        shares = 0
        price = 0
        share_sum = 0
        # Create an array of stocks
        
        
        #redirect("/dashboard")
        
        
        
        
        
        
        
        
        
        
        
        return render_template("dashboard.html",user_name = user[1], current_time = current_time)
            

@app.route("/view")
@login_required
def view():
    print("view user_id:", session.get("user_id"))
    return render_template("view.html")


# Lets a new user register to the site.
@app.route("/register", methods=["GET", "POST"])
def register():
    # user reached route visa Poste (as by submmiting a form via POST)
    # User create an account with username and password
    if request.method == 'POST':
        # Query database for username to see if it already exists
        user_check = db_conn.execute("SELECT * FROM USERS WHERE username = ?", (request.form.get('username'),))
        user_check = user_check.fetchone()
        if user_check is not None:
            return apology("username already exists", 403)
        if request.form.get('password') == '':
            return apology("must provide password", 403)
        if request.form.get('password') != request.form.get('confirmation'):
            return apology("passwords do not match", 403)
        else:
            #Assign username to a new variable
            username = request.form.get('username')
            #Assign password to a new variable
            password = request.form.get('password')
            if True:
                db_conn.execute('INSERT INTO USERS (username, password) VALUES (?, ?)', (username, password))
                db_conn.commit()
                # Render a confirm that account is created
                flash('Account successfully created!', 'success')
                # Redirect user to login page
                return redirect("/login")
    
    return render_template("register.html")

if __name__ == '__main__':
    '''
    CHECK DATABASE BLOCK
    
    #check if database is connected
    conn = create_connection(r"finance.db")
    query = r"""CREATE TABLE IF NOT EXISTS users (
                            id integer PRIMARY KEY,
                            username text NOT NULL,
                            password text NOT NULL
                            );"""                   
    if conn is not None:
        create_table(conn, query)
    #if conn is not None:
        #insert(conn, "INSERT INTO users (id, username, password) VALUES (?, ?, ?)", ("3","tommy", "admin"))
    res = conn.execute("SELECT * FROM USERS")  
    for row in res:  
        print(row)   
    conn.commit()           
    conn.close()
    '''    
        
    '''
    RUN FLASK BLOCK
    '''    
    app.run(host='localhost', port=8080, debug=True)