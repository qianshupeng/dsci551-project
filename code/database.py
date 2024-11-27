# database.py
# Interact with mysql database

import pymysql
import pandas as pd
import json
import re
from config import connect_to_server, connect_to_database
from utils import infer_column_types

def validate_foreign_key_format(foreign_key):
    """Validate the foreign key format."""
    if foreign_key.lower() == "none":
        return True

    # Check each foreign key definition
    fk_pattern = re.compile(r"^\s*\w+\s*:\s*\w+\(\w+\)\s*$")
    fk_entries = foreign_key.split(",")
    for fk in fk_entries:
        if not fk_pattern.match(fk.strip()):
            return False
    return True

def create_database(database_name):
    """Create a new MySQL database if it doesn't exist."""
    connection = connect_to_server()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        connection.commit()
        print(f"Database '{database_name}' created successfully!")

    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")

    finally:
        connection.close()


def create_table_from_csv(connection, database_name, table_name, csv_file_path, primary_key : str, foreign_key="None", data_types="None"):
    """Create a table in the current database from a CSV file and insert its data."""
    try:
        # Load CSV data
        df = pd.read_csv(csv_file_path)

        # Analyze data type if not entered
        if data_types.lower() == "none":
            data_types = infer_column_types(df)
        else:
            data_types = data_types.split(",")

        if len(data_types) != len(df.columns):
            print("Error: Number of data types does not match number of columns!")
            return
        
        if not validate_foreign_key_format(foreign_key):
            print(f"Error: Foreign key format is invalid for table '{table_name}'. Expected format: 'col1: table1(col), col2: table2(somecol)'")
            return
        
        # Construct CREATE statement
        full_table_name = f"`{database_name}`.`{table_name}`"
        column_definitions = ", ".join(
            [f"`{col}` {dtype}" for col, dtype in zip(df.columns, data_types)]
        )
        create_table_query = f"CREATE TABLE {full_table_name} ({column_definitions}, PRIMARY KEY (`{primary_key}`)"

        # Add foreign keys if needed
        if foreign_key.lower() != "none":
            fk_constraints = []
            for fk in foreign_key.split(","):
                fk_col, ref = fk.split(":")
                table_name_ref, col_name_ref = re.match(r"(\w+)\((\w+)\)", ref.strip()).groups()
                fk_constraints.append(
                    f"FOREIGN KEY (`{fk_col.strip()}`) REFERENCES `{database_name}`.`{table_name_ref.strip()}`(`{col_name_ref.strip()}`)"
                )
            create_table_query += ", " + ", ".join(fk_constraints)

        create_table_query += ");"

        # Create table
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)

        # Add data
        for _, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {full_table_name} ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({placeholders});"
            with connection.cursor() as cursor: 
                cursor.execute(insert_query, tuple(row))

        connection.commit()
        print(f"Table '{table_name}' created and data inserted!")

        # Save table metadata to JSON
        table_metadata = {
            "columns": list(df.columns),
            "primary_key": primary_key.split(","),
            "foreign_key": foreign_key,
            "data_types": data_types,
            "quantitative": [
                col for col, dtype in zip(df.columns, data_types) if dtype.upper() in {"INT", "FLOAT"}
            ],
            "categorical": [
                col for col, dtype in zip(df.columns, data_types) if dtype.upper() not in {"INT", "FLOAT"}
            ],
        }
        with open(f"{table_name}_metadata.json", "w") as f:
            json.dump(table_metadata, f, indent=4)

    except pymysql.MySQLError as e:
        print(f"Error creating table or inserting data: {e}")
