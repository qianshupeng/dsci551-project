# main.py
# Interface and main running logic of ChatDB

import sys
import os
import json
from config import save_db_config, connect_to_database, load_db_config
from database import create_database, create_table_from_csv
from utils import is_valid_file, get_table_name
from query import explore_database, describe_table, generate_sample_queries
from nlp import generate_query_from_nlp

HOST = None
USER = None
PASSWORD = None

CONFIG_FILE = "db_config.json"
BUILTIN_DATABASE = "builtin_db"
BUILTIN_DATASETS = [
     {"path": "../data/stores.csv", "primary_key": "store_id", 
      "foreign_key": "None", 
      "data_types": "INT, VARCHAR(100)"}, 
     {"path": "../data/products.csv", "primary_key": "product_id", 
      "foreign_key": "None", 
      "data_types": "INT, FLOAT, VARCHAR(100), VARCHAR(100), VARCHAR(100)"},
     {"path": "../data/transactions.csv", "primary_key": "transaction_id", 
      "foreign_key": "store_id: stores(store_id), product_id: products(product_id)", 
      "data_types": "INT, DATE, TIME, INT, INT, INT"}
     ]

if __name__ == "__main__":
    print("Welcome to ChatDB! \nBy Qianshu Peng")

    # initialization built-in database and datasets
    print("Initialization...")
    if not os.path.exists(CONFIG_FILE):
        save_db_config(HOST, USER, PASSWORD)
    else:
        print("Reading MySQL Configuration...")
        config = load_db_config()
    create_database(BUILTIN_DATABASE)
    connection = connect_to_database(BUILTIN_DATABASE)

    for dataset in BUILTIN_DATASETS:
        if is_valid_file(dataset["path"]):
            table_name = get_table_name(dataset["path"])
            create_table_from_csv(
                connection,
                BUILTIN_DATABASE, 
                table_name,
                dataset["path"],
                dataset["primary_key"],
                dataset["foreign_key"],
                dataset["data_types"]
            )
        else:
            print(f"Skipping invalid file: {dataset['path']}")


    while True:
        print("\nOptions: \n[1] Explore Built-in Database \n[2] Upload Your Database \n[3] Exit")
        choice1 = input("Select an option: ")

        if choice1 == "1":
            print("\nChoose a Built-in Database: [1] sales")
            db_choice = input("Select an option: ")
            connection = connect_to_database(BUILTIN_DATABASE)
            status1 = True
            while status1:
                choice2 = input("Built-in Database: [1] Explore all tables \n[2] Select a table \n[3] Exit \n")

                if choice2 == "1":
                    explore_database(connection)

                elif choice2 == "2":
                    table_name = input("Enter the table name: ")
                    describe_table(connection, table_name)

                    while True:
                        print("\nTable Options: \n[1] Generate sample queries \n[2] Enter NLP query \n[3] Back to table selection")
                        table_choice = input("Select an option: ")

                        if table_choice == "1":
                            generate_sample_queries(connection, table_name)

                        elif table_choice == "2":
                            nlp_input = input("Enter your NLP query (check documentation for examples): ")
                            generate_query_from_nlp(connection, table_name, nlp_input)
                            
                        elif table_choice == "3":
                            break

                        else:
                            print("Invalid input.")

                elif choice2 == "3":
                    status1 = False
                else:
                    print("Invalid input.")

        elif choice1 == "2":
            db_name = input("Enter your database name: ")
            create_database(db_name)
            connection = connect_to_database(db_name)
            print("Important: If there exists reference relationships (i.e. foreign keys), please enter the file which referencing others after all the referenced ones. ")
            file_path = input("Enter comma-separated list of CSV file pathes (table name will be the file name): ")
            for file in file_path.split(","):
                file = file.strip()
                if is_valid_file(file):
                    table_name = get_table_name(file)
                    primary_key = input(f"Enter primary key(s) for table '{table_name}' (comma-separated): ")
                    foreign_key = input(f"Enter foreign key(s) for table '{table_name}' (format: 'col1: table1(col), col2: table2(column)', None if no foreign key): ")
                    data_types = input(f"Enter data types for columns in table '{table_name}' (comma-separated or 'None' to infer): ")

                    create_table_from_csv(
                        connection,
                        db_name, 
                        table_name,
                        file,
                        primary_key,
                        foreign_key,
                        data_types
                    )
                else:
                    print("Invalid file. Please provide valid CSV(s).")

            status2 = True
            while status2:
                print("\nUploaded Database Options: \n[1] Explore all tables \n[2] Select a table \n[3] Exit")
                choice3 = input("Select an option: ")

                if choice3 == "1":
                    explore_database(connection)

                elif choice3 == "2":
                    table_name = input("Enter the table name to describe: ")
                    describe_table(connection, table_name)

                    while True:
                        print("\nTable Options: \n[1] Generate sample queries \n[2] Enter NLP query \n[3] Back to table selection")
                        table_choice = input("Select an option: ")

                        if table_choice == "1":
                            generate_sample_queries(connection, table_name)

                        elif table_choice == "2":
                            nlp_input = input("Enter your NLP query: ")
                            generate_query_from_nlp(connection, table_name, nlp_input)

                        elif table_choice == "3":
                            break
                        else:
                            print("Invalid input.")

                elif choice3 == "3":
                    status2 = False
                else:
                    print("Invalid input.")

        elif choice1 == "3":
            print("Goodbye! :)")
            try: 
                connection.close()
            except:
                continue
            sys.exit()
        
        else:
            print("Invalid Input. Please check the documentation for instructions. ")