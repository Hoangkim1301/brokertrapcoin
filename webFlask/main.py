import os

import sqlite3
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
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def hello_world():
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
        
        #check if username exists
        user = db_conn.execute("SELECT * FROM USERS WHERE username = ?", (username,))
        
        for row in user:  
            if len(row) == 0 or (row[2] != password):
                return apology("invalid username and/or password", 403)
            elif row[2] == password:
                # Remember which user has logged in.
                session["user_id"] = row[0]
                return dashboard()
            
    else:    
        return render_template("login.html")

@app.route("/logout",methods=['POST', 'GET'])
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return render_template("logout.html")

@app.route("/dashboard")
@login_required
def dashboard():
    #identify current user
    user_id = session["user_id"]
    
    
    return render_template("dashboard.html")

@app.route("/index")
def index():
    return render_template("index.html")


# Lets a new user register to the site.
@app.route("/register", methods=["GET", "POST"])
def register():
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