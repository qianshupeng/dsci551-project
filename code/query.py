# query.py
# Take patterns, return queries; give sample queries

import re
import pymysql
import random

def explore_database(connection):
    """Print the structure of all tables in the connected database."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                print("No tables found in the database.")
                return

            for table in tables:
                print(f"\nStructure of table `{table}`:")
                cursor.execute(f"DESC `{table}`;")
                result = cursor.fetchall()
                for row in result:
                    print(row)
    except pymysql.MySQLError as e:
        print(f"Error exploring database: {e}")


def describe_table(connection, table_name):
    """Describe the structure of a specific table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DESC `{table_name}`;")
            result = cursor.fetchall()
            print(f"\nStructure of table `{table_name}`:")
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error describing table `{table_name}`: {e}")


def generate_sample_queries(connection, table_name):
    """Generate and execute random sample queries for a specific table in the database."""
    import random

    try:
        with connection.cursor() as cursor:
            # Get the column names and data types for the given table
            cursor.execute(f"DESCRIBE `{table_name}`;")
            columns_info = cursor.fetchall()

            if not columns_info:
                print(f"No columns found in table `{table_name}`.")
                return

            # Extract column names and data types
            column_names = [col[0] for col in columns_info]
            column_types = [col[1] for col in columns_info]

            # Define possible patterns for sample queries
            sample_queries = []

            # Add a query for selecting all rows with a limit
            sample_queries.append({
                "description": "Select all rows with a limit",
                "query": f"SELECT * FROM `{table_name}` LIMIT 5;"
            })

            # Add a query for counting the number of rows in the table
            sample_queries.append({
                "description": "Count the number of rows in the table",
                "query": f"SELECT COUNT(*) FROM `{table_name}`;"
            })

            # Add a query for selecting a random sample of rows
            sample_queries.append({
                "description": "Select a random sample of rows",
                "query": f"SELECT * FROM `{table_name}` ORDER BY RAND() LIMIT 3;"
            })

            # Add a group by query if a numeric column exists
            for col_name, col_type in zip(column_names, column_types):
                if "int" in col_type.lower() or "float" in col_type.lower():
                    sample_queries.append({
                        "description": f"Group by {col_name} and calculate sum",
                        "query": f"SELECT `{col_name}`, SUM(`{col_name}`) FROM `{table_name}` GROUP BY `{col_name}`;"
                    })
                    break  # Assuming we only need one numeric column for SUM

            # Add where condition queries based on numeric columns
            for col_name, col_type in zip(column_names, column_types):
                if "int" in col_type.lower() or "float" in col_type.lower():
                    sample_queries.append({
                        "description": f"Select rows where {col_name} is greater than 10",
                        "query": f"SELECT * FROM `{table_name}` WHERE `{col_name}` > 10;"
                    })

                    sample_queries.append({
                        "description": f"Select rows where {col_name} is between 10 and 50",
                        "query": f"SELECT * FROM `{table_name}` WHERE `{col_name}` BETWEEN 10 AND 50;"
                    })
                    break  # Only need one numeric column for the conditions

            # Add distinct queries for all columns (including non-numeric columns)
            for col_name in column_names:
                sample_queries.append({
                    "description": f"Select distinct values from {col_name}",
                    "query": f"SELECT DISTINCT `{col_name}` FROM `{table_name}`;"
                })

            # Randomly shuffle the queries to show a variety
            chosen_queries = random.sample(sample_queries, 5)

            print("\nGenerated Sample Queries:")
            for idx, query_info in enumerate(chosen_queries, 1):
                print(f"{idx}. {query_info['description']}:\n{query_info['query']}\n")


            # Allow user to select a query to run
            choice = input("Enter the query number to execute (or '0' to cancel): ")
            if choice.isdigit() and 0 < int(choice) <= len(chosen_queries):
                query_to_execute = chosen_queries[int(choice) - 1]["query"]
                print(f"\nExecuting Query: {query_to_execute}")
                cursor.execute(query_to_execute)
                result = cursor.fetchall()
                print("\nQuery Result:")
                for row in result:
                    print(row)
            elif choice == "0":
                print("Cancelled.")
            else:
                print("Invalid input.")
    except Exception as e:
        print(f"Error generating or executing sample queries: {e}")




def generate_sample_queries_notused(connection, table_name):
    """Generate and execute random sample queries for tables in the database."""
    import random

    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                print("No tables found in the database.")
                return

            sample_queries = []
            for table in tables:
                sample_queries.append(f"SELECT * FROM `{table}` LIMIT 5;")
                sample_queries.append(f"SELECT COUNT(*) FROM `{table}`;")
                sample_queries.append(f"SELECT * FROM `{table}` ORDER BY RAND() LIMIT 3;")

            chosen_queries = random.sample(sample_queries, min(len(sample_queries), 5))
            print("\nGenerated Sample Queries:")
            for idx, query in enumerate(chosen_queries, 1):
                print(f"{idx}. {query}")

            choice = input("\nEnter the query number to execute (or '0' to cancel): ")
            if choice.isdigit() and 0 < int(choice) <= len(chosen_queries):
                query_to_execute = chosen_queries[int(choice) - 1]
                cursor.execute(query_to_execute)
                result = cursor.fetchall()
                print("\nQuery Result:")
                for row in result:
                    print(row)
            elif choice == "0":
                print("Cancelled.")
            else:
                print("Invalid input.")
    except Exception as e:
        print(f"Error generating or executing sample queries: {e}")

