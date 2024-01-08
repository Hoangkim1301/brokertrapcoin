# Stock Trading Website

# A helper file to be used in conjunction with application.py.

import os
import requests
import urllib.parse

import yfinance as yf
from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime, timedelta

#api_key = 'pk_c5d6f2b09e8a40fcb45ae5a0f58fcbb6'


# Render message as an apology to user.
def apology(message, code=400):
    def escape(s):
        # Escape special characters.
        # https://github.com/jacebrowning/memegen#special-characters
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Decorate routes to require login.
# http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Look up quote for symbol.
def lookup_iex_api(symbol):
    api_key = os.environ.get("API_KEY")
    # Contact API.
    try:
        #response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        #response.raise_for_status()       
        endpoint = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}'
        
        # Sending a GET request to the endpoint
        response = requests.get(endpoint)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            stock_data = response.json()
            stock_info = {
                'name': stock_data.get('companyName'),
                'symbol': stock_data.get('symbol'),
                'latest_price': stock_data.get('latestPrice')
            }
            return stock_info
    except requests.RequestException:
        return None
    except (KeyError, TypeError, ValueError):
        return None

def lookup_yfinance(stock_code):
    try:
        # Calculate the start date as one month ago from today
        start_date = datetime.now() - timedelta(days=7)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')


        data = yf.download(tickers=stock_code, start=start_date, end=end_date, interval='1d', auto_adjust=True)
        price = data['Close'].iloc[-1]  # Get the latest price at the last minute

        # Fetch the company's info to get the full name
        ticker = yf.Ticker(stock_code)
        company_info = ticker.info
        full_name = company_info['longName'] if 'longName' in company_info else stock_code

        stock_info = {
            'name': full_name,
            'symbol': stock_code,
            'latest_price': round(price, 2)
        }
        
        return stock_info

    except Exception as e:
        print(f'Failed to fetch data: {e}')
        return None

def bought_calc(stock_symbol, user_id,db_conn):
    # Get the number of shares for the stock in this loop ( which are belongs to current users ) from stocks table
    # Then add them to get the total number of shares for the stocks
    shares_sum = db_conn.execute("SELECT SUM(shares) FROM stocks WHERE symbol = ? AND user_id = ?", (stock_symbol, user_id)).fetchone()[0] 
    print("shares_sum: ", shares_sum)
    # If we have more or equals 1 share of this stock ()
    if shares_sum >= 1:
        # Get the total price of this stock
        total_price = db_conn.execute("SELECT SUM(price) FROM stocks WHERE symbol = ? AND user_id = ?", (stock_symbol, user_id)).fetchone()[0]
        # Calculate the average price of this stock
        bought = total_price / shares_sum
        # Round the average price to 2 decimal places
        bought = round(bought,2)
        return bought
    else:
        return None

# Format value as USD.
def usd(value):
    return ("value: ", value)

def usd_to_euro(value):
    #calculate euro value
    value = value * 0.85
    return f"€{value:,.2f}"

#main
if __name__ == '__main__':
    price = lookup_yfinance('AAPL')
    print('price:', price)