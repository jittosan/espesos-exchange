'''
------------------------------------------

        WEB/API SERVER - ESPesos Exchange

------------------------------------------

API endpoints process transactions with database

'''

##  SERVER CONFIGURATION
PORT = 8000
PRODUCTION_SERVER = True

# import dependencies
from flask import Flask, request, json
from database_handler import ExchangeDatabase
from utils import *

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
    data = json.loads(request.data)
    output = {}
    
    #token not found
    if not check_keys(data, ['sender_token', 'recipient_token', 'amount']):
        output['status'] = 400
        output['error'] = 'Incomplete data fields entered'
    else:
        sender_token = data['sender_token']
        recipient_token = data['recipient_token']
        amount = float(data['amount'])
        # both tokens do not exist
        if not exchange.check_account(sender_token) or not exchange.check_account(recipient_token):
            output['status'] = 404
            output['error'] = 'Invalid tokens - not found'
        #sender and recipient are identical
        elif sender_token == recipient_token:
            output['status'] = 400
            output['error'] = 'Invalid tokens - repeated'
        #negative amounts entered
        elif amount < 0:
            output['status'] = 404
            output['error'] = 'Invalid amount'
        #check sender account enough balance
        elif not exchange.check_account_balance(sender_token, amount):
            output['status'] = 401
            output['error'] = 'Insufficient funds'
        else:
            #execute transaction
            exchange.add_transaction({
                'sender_token':sender_token,
                'recipient_token':recipient_token,
                'amount':amount
            })
            exchange.update_account_balance(sender_token, amount*-1)
            exchange.update_account_balance(recipient_token, amount)
            #commit changes in production
            if PRODUCTION_SERVER:
                exchange.commit()
            output['status'] = 200
    #return response
    return output

# Account Info
@app.route("/account/", methods=['POST'])
def account():
    data = json.loads(request.data)
    output = {}
    #token not found
    if not check_keys(data, ['token']):
        output['status'] = 400
        output['error'] = 'No token found'
    else:
        token = data['token']
        #token found, but invalid
        if not exchange.check_account(token): 
            output['status'] = 404
            output['error'] = 'Invalid token'
        else:
            output = exchange.get_account(token)
            output['status'] = 200
    #return response
    return output

# run server
app.run(port=PORT)