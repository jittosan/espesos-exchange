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
    data = json.loads(request.data)
    output = {}
    #token not found
    if "token" not in data.keys():
        output = {'error': 'No token found'}
    else:
        #check for invalid token
        token = data['token']
        print("Token Found: " + token)
        output = exchange.get_account(token)
    return output

app.run(port=PORT)