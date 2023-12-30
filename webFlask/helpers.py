# Stock Trading Website

# A helper file to be used in conjunction with application.py.

import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

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
def lookup(symbol):
    api_key = ''
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


# Format value as USD.
def usd(value):
    return ("value: ", value)

def usd_to_euro(value):
    #calculate euro value
    value = value * 0.85
    return f"€{value:,.2f}"

#main
if __name__ == '__main__':
    lookup('AAPL')