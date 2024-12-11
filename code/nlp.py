# nlp.py
# Natural language processing

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')

def lemmatize_input(input_text):
    """Tokenize and lemmatize the input text."""
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(input_text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_tokens


def execute_query(connection, query):
    """Execute the generated SQL query and print results."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            print("\nQuery Result:")
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error executing query: {e}")


def generate_query_from_nlp(connection, table_name, nlp_input):
    """Generate and execute SQL query based on NLP input."""
    lemmatized_input = lemmatize_input(nlp_input)

    # Pattern matching for common queries
    if 'by' in lemmatized_input:
        if 'total' in lemmatized_input:
        # e.g., "total A by B"
            match = re.search(r'total (\w+) by (\w+)', nlp_input)
            if match:
                metric, category = match.groups()
                query = f"SELECT {category}, SUM({metric}) FROM `{table_name}` GROUP BY {category};"
                print(f"Generated Query:\n{query}")
                execute_query(connection, query)
        elif 'average' in lemmatized_input:
            match = re.search(r'average (\w+) by (\w+)', nlp_input)
            if match:
                metric, category = match.groups()
                query = f"SELECT {category}, AVG({metric}) FROM `{table_name}` GROUP BY {category};"
                print(f"Generated Query:\n{query}")
                execute_query(connection, query)
        elif 'count' in lemmatized_input:
            match = re.search(r'count (\w+) by (\w+)', nlp_input)
            if match:
                metric, category = match.groups()
                query = f"SELECT {category}, COUNT({metric}) FROM `{table_name}` GROUP BY {category};"
                print(f"Generated Query:\n{query}")
                execute_query(connection, query)

    elif 'where' in lemmatized_input:
        # e.g., "A where X greater than 10" or "where X = 'some_value'"
        match = re.search(r'where (\w+) (>=|<=|>|<|=) (".*"|\d+)', nlp_input)
        if match:
            column, operator, value = match.groups()
            # Remove the quotes if it's a string value
            value = value.strip('"') if value.startswith('"') else value
            if not value.isnumeric():
                value = "\'" + value + "\'"
            query = f"SELECT * FROM `{table_name}` WHERE `{column}` {operator} {value};"
            print(f"Generated Query:\n{query}")
            execute_query(connection, query)

        # Handle BETWEEN pattern: "where X between 10 and 20"
        match = re.search(r'where (\w+) between (\d+) and (\d+)', nlp_input)
        if match:
            column, lower, upper = match.groups()
            query = f"SELECT * FROM `{table_name}` WHERE `{column}` BETWEEN {lower} AND {upper};"
            print(f"Generated Query:\n{query}")
            execute_query(connection, query)

        # Handle LIKE pattern: "where name like '%value%'"
        match = re.search(r'where (\w+) like "(.*)"', nlp_input)
        if match:
            column, pattern = match.groups()
            query = f"SELECT * FROM `{table_name}` WHERE `{column}` LIKE '%{pattern}%';"
            print(f"Generated Query:\n{query}")
            execute_query(connection, query)

    elif 'count' in lemmatized_input:
        # e.g., "count X where X > 10"
        match = re.search(r'count (\w+) where (\w+) (>=|<=|>|<|=) (".*"\d+)', nlp_input)
        if match:
            table, column, operator, value = match.groups()
            query = f"SELECT COUNT(`{table}`) FROM `{table_name}` WHERE `{column}` {operator} {value};"
            print(f"Generated Query:\n{query}")
            execute_query(connection, query)

    else:
        print("Could not match the input pattern.")

