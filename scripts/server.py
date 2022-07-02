'''
------------------------------------------

        WEB/API SERVER - ESPesos Exchange

------------------------------------------

API endpoints process transactions with database

'''

##  SERVER CONFIGURATION
PORT = 8000

# import dependencies
from flask import Flask, request, json
from database_handler import ExchangeDatabase
from server_utils import *

# define utility functions
def check_keys(data, keys=[]):
    # return False if any key is missing
    for item in keys:
        if item not in data:
            return False
    # return True if all keys present
    return True

# initalise app
app = Flask(__name__)
exchange = ExchangeDatabase()

# Home
@app.route("/")
def home():
    return "<h1>ESPesos Exchange Homepage</h1>"

# Transaction
@app.route("/transaction/", methods=['POST'])
def transact():
    #invalid format error
    #verify both tokens valid
    #check sender account enough balance
    
    return "<h1>Transact ESPesos</h1>"

# Account Info
@app.route("/account/", methods=['POST'])
def account():
    print("ACCOUNT ENDPOINT")
    data = json.loads(request.data)
    output = {}
    #token not found
    if not check_keys(data, ['token']):
        print("TOKEN NOT FOUND")
        output['status'] = 400
        output['error'] = 'No token found'
    else:
        print("TOKEN found")
        token = data['token']
        results = exchange.get_account(token)
        #token found, but invalid
        if results == {}:
            print("TOKEN INVALID")
            output['status'] = 404
            output['error'] = 'Invalid token'
        else:
            output = results
            output['status'] = 200
    #return response
    return output

# run server
app.run(port=PORT)