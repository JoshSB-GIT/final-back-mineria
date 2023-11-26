from flask_mysqldb import MySQL
from flask import Flask


class DataBase():
    app = Flask(__name__)
    conn = MySQL(app)
