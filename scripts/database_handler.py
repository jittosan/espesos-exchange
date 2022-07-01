'''
DATABASE FUNCTIONS

'''
## CONFIGURATION PARAMETERS
PATH_TO_DATA = "../data"
EXCHANGE_DATABASE = "exchange.db"


#import dependencies
import sqlite3 as sq

##HIGHER LEVEL USE FUNCTIONS
def add_account():
    pass

def remove_account():
    pass

def get_account():
    pass

def search_account():
    pass

def transact():
    pass

def find_transaction():
    pass

def find_transaction_raw():
    pass


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