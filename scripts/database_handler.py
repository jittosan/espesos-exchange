'''
DATABASE FUNCTIONS

'''
## CONFIGURATION PARAMETERS
PATH_TO_DATA = "../data/"
EXCHANGE_DATABASE = "exchange.db"

#import dependencies
import sqlite3 as sq
from utils import *
class ExchangeDatabase():
    def __init__(self):
        self._db = None
        self._cursor = None
        self.connect()

    ## low-level database functions

    def connect(self):
        #return True if already connected
        if self.connected():
            return True
        try:
            self._db = sq.connect(PATH_TO_DATA + EXCHANGE_DATABASE, check_same_thread=True)
            self._cursor = self._db.cursor()
            print("Exchange Database connected successfully.")
            return True
        except sq.Error as e:
            print("Exchange Database failed to connect.")
            print(e)
            return False

    def disconnect(self):
        self.commit()
        self._db.close()
        self._db = None
        self._cursor = None
        print("Exchange Database disconnected successfully.\n")
        return True

    def connected(self):
        return self._db != None

    def query(self, query_string):
        #check if database already connected
        if not self.connected():
            return False
        
        results = None
        try:
            self._cursor.execute(query_string)
            results = self._cursor.fetchall()
        except sq.Error as e:
            print("Query Failed : " + query_string)
            print(e)
        finally:
            return results   

    def execute(self, command_string):
        #check if database already connected
        if not self.connected():
            return False
        
        results = None
        try:
            results = self._cursor.execute(command_string)
        except sq.Error as e:
            print("Execution Failed : " + command_string)
            print(e)
        finally:
            return results != None  

    def commit(self):
        if not self.connected():
            return False
        self._db.commit()
        return True

    ## utility methods fo data manipulation

    def parse_account(self, query_value):
        if query_value == []:
            values = {}
        else:
            values ={
                'token': query_value[0][0],
                'name': query_value[0][1],
                'fingerprint': query_value[0][2],
                'balance': float(query_value[0][3])
            }
        return values

    def parse_transaction(self, query_value):
        if query_value == []:
            values = {}
        else:
            values ={
                'transaction_id': int(query_value[0][0]),
                'sender_token': query_value[0][1],
                'recipient_token': query_value[0][2],
                'amount': float(query_value[0][3])
            }
        return values

    ## account interface methods

    def add_account(self, values):
        #check all fields have been input
        if not check_keys(values, ['token', 'name', 'fingerprint', 'balance']):
            return False
        return self.execute("INSERT INTO accounts VALUES ('{token}', '{name}', '{fingerprint}', {balance})".format(
            token=values['token'], name=values['name'], fingerprint=values['fingerprint'], balance=values['balance']))

    def remove_account(self, token):
        return self.execute("DELETE * from accounts WHERE token='{token}'".format(token=token))

    def get_account(self, token):
        return self.parse_account(self.query('SELECT * from accounts WHERE token="{token}"'.format(token=token)))

    def get_account_info(self, token):
        results = self.get_account(token)
        if results != {}:
            del results['fingerprint']
        return results

    def check_account(self, token):
        return self.query('SELECT * from accounts WHERE token="{token}"'.format(token=token)) != []

    def verify_fingerprint(self, token, fingerprint):
        results = self.get_account(token)
        if results != {}:
            return fingerprint == results['fingerprint']
        else:
            return False

    def get_account_balance(self, token):
        results = self.get_account(token)
        if results == {}:
            return None
        else:
            return results['balance']

    def update_account_balance(self, token, delta):
        if not self.connected():
            return False

        #query db, return False if no records found
        old_balance = self.get_account_balance(token)
        if old_balance == None:
            return False

        new_balance = old_balance + delta
        return self.execute("UPDATE accounts SET balance='{new_balance}' WHERE token='{token}'".format(token=token, new_balance=new_balance))

    def check_account_balance(self, token, amount):
        return self.get_account_balance(token) >= amount

    def search_account(self, name):
        return self.parse_account(self.query("SELECT * from accounts WHERE name='{name}'".format(name=name)))

    ## transaction interface methods

    def add_transaction(self, values):
        #check all fields have been input
        if not check_keys(values, ['sender_token', 'recipient_token', 'amount']):
            return False
        return self.execute("INSERT INTO transactions (sender_token, recipient_token, amount) VALUES ('{sender_token}', '{recipient_token}', '{amount}')".format(
            sender_token=values['sender_token'], recipient_token=values['recipient_token'], amount=values['amount']))

    def remove_transaction(self, transaction_id):
        return self.query("DELETE * from transactions WHERE transaction_id='{transaction_id}'".format(transaction_id=transaction_id))

    def get_transaction(self, transaction_id):
        return self.parse_transaction(self.query("SELECT * from transactions WHERE transaction_id='{transaction_id}'".format(transaction_id=transaction_id)))

    def find_transaction(self, sender_token, recipient_token):
        return self.parse_transaction(self.query("SELECT * from transactions WHERE sender_token='{sender_token}' & recipient_token='{recipient_token}'".format(sender_token=sender_token, recipient_token=recipient_token)))