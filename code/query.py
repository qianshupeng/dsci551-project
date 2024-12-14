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
    numerics = ["int", "float", "datetime", "date", "time"]

    try:
        with connection.cursor() as cursor:
            # Get the column names and data types for the given table
            cursor.execute(f"DESCRIBE `{table_name}`;")
            columns_info = cursor.fetchall()

            # Get foreign keys
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`;")
            create_table_info = cursor.fetchone()[1]
            foreign_keys = []
            for line in create_table_info.split("\n"):
                if "CONSTRAINT" in line and "FOREIGN KEY" in line:
                    fk_match = re.search(r"FOREIGN KEY \(`(\w+)`\) REFERENCES `(\w+)` \(`(\w+)`\)", line)
                    if fk_match:
                        fk_col, ref_table, ref_col = fk_match.groups()
                        foreign_keys.append((fk_col, ref_table, ref_col))

            if not columns_info:
                print(f"No columns found in table `{table_name}`.")
                return

            # Extract column names and data types
            column_names = [col[0] for col in columns_info]
            column_types = [col[1] for col in columns_info]

            # Define possible patterns for sample queries
            sample_queries = []

            # Add a query for selecting all rows with a limit
            limit = random.randint(1, 50)
            sample_queries.append({
                "description": "Select all rows with a limit",
                "query": f"SELECT * FROM `{table_name}` LIMIT {limit};"
            })

            # Add a query for counting the number of rows in the table
            sample_queries.append({
                "description": "Count the number of rows in the table",
                "query": f"SELECT COUNT(*) FROM `{table_name}`;"
            })

            # Add a query for selecting a random sample of rows
            sample_queries.append({
                "description": "Select a random sample of rows",
                "query": f"SELECT * FROM `{table_name}` ORDER BY RAND() LIMIT 10;"
            })

            # Add a query with order by
            for col_name, col_type in zip(column_names, column_types):
                if col_type.lower() in numerics:
                    sample_queries.append({
                        "description": f"Select all rows order by {col_name}",
                        "query": f"SELECT * FROM `{table_name}` ORDER BY `{col_name}`;"
                    })

                    rand_col = random.sample(column_names, k=random.randint(1, len(column_names)))
                    rand_col_str = "`,`".join(list(rand_col))
                    sample_queries.append({
                        "description": f"Select column(s) {rand_col} order by {col_name}",
                        "query": f"SELECT `{rand_col_str}` FROM `{table_name}` ORDER BY `{col_name}`;"
                    })
            
            # Add group by queries if numeric columns exist
            for col_name, col_type in zip(column_names, column_types):
                if col_type.lower() in numerics:
                    for col_cate, cate_type in zip(column_names, column_types):
                        if cate_type.lower() not in numerics:
                            sample_queries.append({
                                "description": f"Group by {col_cate} and calculate sum",
                                "query": f"SELECT `{col_cate}`, SUM(`{col_name}`) FROM `{table_name}` GROUP BY `{col_cate}`;"
                            })

                            limit = random.randint(1, 100)
                            sample_queries.append({
                                "description": f"Group by {col_cate} and filter using HAVING",
                                "query": f"SELECT `{col_cate}`, SUM(`{col_name}`) FROM `{table_name}` GROUP BY `{col_cate}` HAVING SUM(`{col_name}`) > {limit};"
                            })
                            break
                else:
                    sample_queries.append({
                        "description": f"Group by {col_name} and count",
                        "query": f"SELECT `{col_name}`, COUNT(`{col_name}`) FROM `{table_name}` GROUP BY `{col_name}`;"
                    })
            # print(sample_queries) #for test

            # Add where condition queries based on numeric columns
            for col_name, col_type in zip(column_names, column_types):
                if col_type.lower() in numerics:
                    limit2 = limit + random.randint(1, 100)
                    sample_queries.append({
                        "description": f"Select rows where {col_name} is greater than {limit}",
                        "query": f"SELECT * FROM `{table_name}` WHERE `{col_name}` > {limit};"
                    })

                    sample_queries.append({
                        "description": f"Select rows where {col_name} is between {limit} and {limit2}",
                        "query": f"SELECT * FROM `{table_name}` WHERE `{col_name}` BETWEEN {limit} AND {limit2};"
                    })
                    break  # Only need one numeric column for the conditions

            # Add distinct queries for all columns (including non-numeric columns)
            for col_name in column_names:
                sample_queries.append({
                    "description": f"Select distinct values from {col_name}",
                    "query": f"SELECT DISTINCT `{col_name}` FROM `{table_name}`;"
                })

            # Add JOIN queries if exists references and show sample
            if foreign_keys:
                for fk_col, ref_table, ref_col in foreign_keys:
                    sample_queries.append({
                        "description": f"Join {table_name} with {ref_table}",
                        "query": f"SELECT * FROM `{table_name}` JOIN `{ref_table}` ON `{table_name}`.`{fk_col}` = `{ref_table}`.`{ref_col}` ORDER BY RAND() LIMIT 10;"
                    })


            # Ask users for keyword
            keyword = input("Enter a keyword to filter queries (e.g., 'group by', 'having', 'where', 'order by', 'sum', 'count', 'join') or press Enter to skip: ").lower()
            if keyword:
                # Filter queries based on the keyword
                filtered_queries = [
                    query for query in sample_queries if keyword in query["query"].lower()
                ]
                if not filtered_queries:
                    print(f"This table does not support queries containing the keyword '{keyword}' due to its data types. Please try other options. ")
                    return
                chosen_queries = random.sample(filtered_queries, min(5, len(filtered_queries)))
            else:
                # Randomly shuffle the queries to show a variety
                chosen_queries = random.sample(sample_queries, min(5, len(sample_queries)))

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


