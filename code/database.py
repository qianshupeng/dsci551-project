# database.py
# interact with mysql database

import pymysql
import pandas as pd
from config import connect_to_server, connect_to_database

def create_database(name):
    """For creating new database when starting the program or uploading new data."""
    connection = connect_to_server()
    try:
        with connection.cursor as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{name}`")
        connection.commit()
        print(f"Database '{name}' created successfully!")
    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")

