import os
import requests
import json
import asyncio
from flask import Flask
import mysql.connector

app = Flask(__name__)

app.config["DEBUG"] = True


@app.route("/")
def index():
    dbConnection()
    return "<p>Hello, World!</p>"


def dbConnection():
    mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='root', database='traccar')
    cur = mydb.cursor()
    cur.execute("SHOW TABLES")

    for i in cur:
        print(i)


if __name__ == '__main__':
    app.run()


