'''
------------------------------------------

        WEB/API SERVER - ESPesos Exchange

------------------------------------------

API endpoints process transactions with database

'''
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>ESPesos Exchange Homepage</h1>"

