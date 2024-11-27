# config.py
# For MySQL database configuration

import pymysql
import os
import json

CONFIG_FILE = "db_config.json"

def save_db_config(host=None, user=None, password=None):
    """Prompt user for MySQL connection details and save them to a config file."""
    if host == None:
        host = input("Enter MySQL host: ")
    if user == None:
        user = input("Enter MySQL username: ")
    if password == None:
        password = input("Enter MySQL password: ")
    config = {
        "host": host,
        "user": user,
        "password": password
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print("MySQL configuration saved!")


def load_db_config():
    """Load MySQL connection details from the config file."""
    if not os.path.exists(CONFIG_FILE):
        print("No database configuration found. Please provide connection details.")
        save_db_config()
    
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    

def connect_to_server():
    """Establish connection to MySQL server using saved configuration."""
    config = load_db_config()
    connection = pymysql.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
    )
    return connection


def connect_to_database(database_name=None):
    """Connect to a specific MySQL database."""
    config = load_db_config()
    connection = pymysql.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=database_name if database_name else None
    )
    return connection
