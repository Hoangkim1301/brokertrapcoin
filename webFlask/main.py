import os
import sqlite3

from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup_iex_api, usd, lookup_yfinance

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

# Make sure API key is set.
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")

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
        #identify current user_name
        user_name = db_conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()[0]
        stock_list = db_conn.execute("SELECT DISTINCT symbol FROM stocks WHERE user_id = ?", (user_id,))
        user_stock = [row[0] for row in stock_list.fetchall()]
           
        # Create a list of stock's information
        stock_info_list = []
        # Initialize variales here for correct scope
        stock_name = ''
        # Create an array of stocks which we already added to the list, prevent duplicates
        stocks_seen = []
        # A list of stock_attributes to be passed to dashboard.html
        all_stocks = []
        # A sum of all the share totals at their current stock price
        share_total = 0
        final_cash = 0
        
        print("user_stock: ", user_stock)
        for row in user_stock:
            # Get stock's name
            stock_symbol = row # symbol
            # Parse the stock information into list
            if stock_symbol in stocks_seen:
                continue
            else:
                # Get stock information from IEX
                #stock_info = lookup_iex_api(stock_symbol)
                stock_info = lookup_yfinance(stock_symbol)
                # Clear stock_info_list 
                stock_info_list.clear()
                # Parse the stock infos to the list
                print("stock_info: ", stock_info)
                for value in stock_info.values():
                    stock_info_list.append(value)
                # Give each index thier appropriate stock information declaration
                stock_name = stock_info_list[0]
                # Get the number of shares for the stock in this loop ( which are belongs to current users ) from stocks table
                # Then add them to get the total number of shares for the stocks
                shares_sum = db_conn.execute("SELECT SUM(shares) FROM stocks WHERE symbol = ? AND user_id = ?", (stock_symbol, user_id)).fetchone()[0] 
                print("shares_sum: ", shares_sum)
                # If we have more or equals 1 share of this stock ()
        
                if shares_sum >= 1:
                    # Add this stock's shares_total to the shares_total_sum to be used in the grand_total calculation.
                    share_total += shares_sum
                    # Calculate price at bought time.
                    bought = db_conn.execute("SELECT SUM(total_price) FROM stocks WHERE symbol = ? AND user_id = ?", (stock_symbol, user_id)).fetchone()[0]
                    # Calculate total price of each stock.
                    total_price = shares_sum * stock_info.get('latest_price')
                    # Calculate final cash
                    final_cash += total_price
                    # Consolidate attributes of this stock to an array.
                    stock_attributes = [stock_symbol, stock_name, shares_sum, bought, stock_info.get('latest_price'),'100%',total_price]
                    # Add this attribute array to the all_stocks array.
                    all_stocks.append(stock_attributes)
                    # Add this stock to the stocks_seen array to prevent duplicates.
                    stocks_seen.append(stock_symbol)

        stocks_seen.clear()
        return render_template("dashboard.html",all_stocks = all_stocks,
                                                share_total_sum = share_total,
                                                final_cash = final_cash,
                                                user_name = user_name, 
                                                current_time = current_time)
            

@app.route("/view")
@login_required
def view():
    print("view user_id:", session.get("user_id"))
    return render_template("view.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'GET':
        return render_template("buy.html")
    
    # User reached route via POST (as by submitting a form via POST)
    else:
        # Get symbol from user input
        symbol = request.form.get('symbol')
        # Get shares from user input
        shares = request.form.get('shares')
        # Lookup for real time stock information via helpers.py
        stock_info = lookup_yfinance(symbol)
        #if the user entered nothing or stock_info is none
        if not symbol or stock_info is None:
            return apology("stock symbol not entered or stock symbol does not exist!", 403)
        # if the user entered nothing or a negative number of shares
        if not shares or int(shares) < 0:
            return apology("share amount was not entered or entry was less than 1.", 403)
        print("stock_info: ", stock_info)
    
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    return render_template("sell.html")

@app.route("/news")
@login_required
def news():
    return render_template("news.html")


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

@app.route("/history")
@login_required
def history():
    return render_template("history.html")

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