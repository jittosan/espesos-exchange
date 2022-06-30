'''
------------------------------------------

        WEB/API SERVER - ESPesos Exchange

------------------------------------------

API endpoints process transactions with database

'''

##  SERVER CONFIGURATION
PORT = 8000



# import dependencies
from flask import Flask



app = Flask(__name__)

# Home
@app.route("/")
def home():
    return "<h1>ESPesos Exchange Homepage</h1>"

# Transaction
@app.route("/transact/")
def transact():
    return "<h1>Transact ESPesos</h1>"

# Account Info
@app.route("/account/")
def account():
    return "<h1>ESPesos Account Information</h1>"

app.run(port=PORT)