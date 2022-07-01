'''
This script initialise all databases required for transactions

'''
import sqlite3 as sq
import os

## UTILITY FUNCTIONS
def create_database(database_name):
    db = None
    try:
        db = sq.connect(database_name)
        print("SUCCESS: {name} created.".format(name=database_name))
    except sq.Error as e:
        print("FAILED: {name} could not be created.".format(name=database_name))
        print(e)
    finally:
        return db

def query_database(database, query_string):
    cursor = database.cursor()
    return cursor.execute(query_string)


## MAIN FUNCTIONS
def initialise_exchange_db():
    print("="*40+"\nInitalising Exchange Database...\n"+"-"*40+"\n")

    #create database exchange.db
    database_name = "exchange.db"
    db = create_database(database_name)
    cursor = db.cursor()

    #create table in database
    try:
        cursor.execute("CREATE TABLE if NOT EXISTS accounts (token PRIMARY KEY, name TEXT NOT NULL, fingerprint TEXT NOT NULL, balance BLOB NOT NULL)")
        print("SUCCESS: {name} created.".format(name='Accounts table'))
    except sq.Error as e:
        print("FAILED: {name} could not be created.".format(name='Accounts table'))
        print(e)

    try:
        cursor.execute("CREATE TABLE if NOT EXISTS transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, sender_token TEXT NOT NULL, recipient_token TEXT NOT NULL, amount BLOB NOT NULL, FOREIGN KEY (sender_token) REFERENCES accounts(token), FOREIGN KEY (recipient_token) REFERENCES accounts(token))")
        print("SUCCESS: {name} created.".format(name='Transactions table'))
    except sq.Error as e:
        print("FAILED: {name} could not be created.".format(name='Transactions table'))
        print(e)

    #close database connection
    db.close()
    print("INITIALISATION COMPLETE: {}".format(database_name))
    print("="*40+"\n")


#access input folder location
path_to_data = "../data/"
os.chdir(path_to_data)
initialise_exchange_db()