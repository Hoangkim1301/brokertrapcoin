import os

#from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

#sys.path.insert(0, './webFlask')
#sys.path.insert(0, './webFlask/templates')

#from picture import picture

app = Flask(__name__, template_folder='webFlask/templates', static_folder='webFlask')

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def hello_world():
    return render_template('/layout.html')

#@app.route("/")
#def index():
#    """Show portfolio of stocks"""
#    return "TODO"

#connect to database
import sqlite3
db = sqlite3.connect('finance.db', check_same_thread=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

# Lets a new user register to the site.
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)