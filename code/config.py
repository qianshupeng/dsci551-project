# config.py
# for MySQL database configuration
import pymysql

def connect_db():
    # connect to the database
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Dsci-551",
        database="dsci551_project"
    )
    return connection
