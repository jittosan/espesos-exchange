'''
DATABASE FUNCTIONS

'''
## CONFIGURATION PARAMETERS
PATH_TO_DATA = "../data"
EXCHANGE_DATABASE = "exchange.db"

#import dependencies
import sqlite3 as sq
class ExchangeDatabase():
    def __init__(self):
        self._db = None
        self._cursor = None
        self.connect()

    def connect(self):
        #return True if already connected
        if self.connected():
            return True
        try:
            self._db = sq.connect(PATH_TO_DATA + EXCHANGE_DATABASE)
            self._cursor = self._db.cursor()
            print("Exchange Database connected successfully.")
            return True
        except sq.Error as e:
            print("Exchange Database failed to connect.")
            print(e)
            return False

    def disconnect(self):
        self._db.close()
        return True

    def connected(self):
        return self._db != None

    def query(self, query_string):
        results = None
        try:
            results = self._cursor.execute(query_string)
        except sq.Error as e:
            print("Query Failed : " + query_string)
            print(e)
        finally:
            return results   

    def add_account(self, values):
        #check all fields have been input
        # if not values.has_key('token') or not values.has_key('name') or not values.has_key('fingerprint') or not values.has_key('balance'):
        #     return False
        self.query("INSERT INTO accounts VALUES ('{token}', '{name}', '{fingerprint}', {balance})".format(
            token=values['token'], name=values['name'], fingerprint=values['fingerprint'], balance=values['balance']))

    def remove_account(self, token):
        return self.query("DELETE * from accounts WHERE token='{token}'".format(token=token))

    def get_account(self, token):
        return self.query("SELECT * from accounts WHERE token='{token}'".format(token=token))

    def search_account(self, name):
        return self.query("SELECT * from accounts WHERE name='{name}'".format(name=name))

    def transact(self, values):
        pass

    def get_transaction(self, transaction_id):
        return self.query("SELECT * from transactions WHERE transaction_id='{transaction_id}'".format(transaction_id=transaction_id))

    def find_transaction(self, sender_token, recipient_token):
        return self.query("SELECT * from transactions WHERE sender_token='{sender_token}' & recipient_token='{recipient_token}'".format(sender_token=sender_token, recipient_token=recipient_token))

## test zone
ex = ExchangeDatabase()
ex.add_account({'token':'A1', 'fingerprint':'A', 'name':"Johnny", "balance":10.0})
print(ex.get_account("A1"))
print(ex.query("SELECT * from transactions"))
