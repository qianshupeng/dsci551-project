# config.py
# for MySQL database configuration
import pymysql

def connect_db():
    # connect to the database
    connection = pymysql.connect()
    return connection
