# nlp.py
# Natural language processing

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

def lemmatize_input(input_text):
    """Tokenize and lemmatize the input text."""
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(input_text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_tokens


def execute_query(connection, query):
    """Execute the generated SQL query and print results."""
    print(f"Generated Query:\n{query}")
    user_input = input("Press Enter to execute the query, or type anything else to cancel: ")
    if user_input.strip() != "":
        print("Query execution cancelled.")
        return

    else:
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

    # Pattern matching for JOIN queries
    if 'join' in lemmatized_input:
        # "col1 in table1 join col2 in table2" or "table1.col1 join table2.col2"
        match = re.search(r'(\w+) in (\w+) join (\w+) in (\w+)', nlp_input)
        if match:
            col1, table1, col2, table2 = match.groups()
            query = f"SELECT * FROM `{table1}` JOIN `{table2}` ON `{table1}`.`{col1}` = `{table2}`.`{col2}`;"
            execute_query(connection, query)

        match = re.search(r'(\w+)\.(\w+) join (\w+)\.(\w+)', nlp_input)
        if match:
            table1, col1, table2, col2 = match.groups()
            query = f"SELECT * FROM `{table1}` JOIN `{table2}` ON `{table1}`.`{col1}` = `{table2}`.`{col2}`;"
            execute_query(connection, query)
        
    # Pattern matching for other special queries
    elif 'by' in lemmatized_input:
        agg_functions = ['total', 'sum', 'average', 'count', 'max', 'largest', 'min', 'smallest']
        dct = {
                'total': 'SUM', 'sum': 'SUM',
                'average': 'AVG',
                'count': 'COUNT',
                'max': 'MAX', 'largest': 'MAX',
                'min': 'MIN', 'smallest': 'MIN'
            }
        for func in agg_functions:
            if func in lemmatized_input:
                match = re.search(fr'{func} (\w+) by (\w+)', nlp_input)
                if match:
                    metric, category = match.groups()
                    sql_func = dct[func]
                    query = f"SELECT `{category}`, {sql_func}(`{metric}`) FROM `{table_name}` GROUP BY `{category}`;"
                    execute_query(connection, query)
    
    elif ('count' in lemmatized_input) and ('where' in lemmatized_input):
        # e.g., "count X where X > 10"
        match = re.search(r'count (\w+) where (\w+) (>=|<=|>|<|=) (".*"|\d+)', nlp_input)
        if match:
            table, column, operator, value = match.groups()
            value = value.strip('"') if value.startswith('"') else value
            if not value.isnumeric():
                value = f"'{value}'"
            query = f"SELECT COUNT(`{table}`) FROM `{table_name}` WHERE `{column}` {operator} {value};"
            execute_query(connection, query)

    elif 'where' in lemmatized_input:
        # e.g., "A where X greater than 10" or "where X = 'some_value'"
        if 'between' in lemmatized_input or 'from' in lemmatized_input:
            # Handle BETWEEN pattern: "where X between 10 and 20" or "where X from 10 to 20"
            match = re.search(r'where (\w+) (between|from) (\d+) (and|to) (\d+)', nlp_input)
            if match:
                column, _, lower, _, upper = match.groups()
                query = f"SELECT * FROM `{table_name}` WHERE `{column}` BETWEEN {lower} AND {upper};"
                execute_query(connection, query)
        elif 'like' in lemmatized_input:
            # Handle LIKE pattern: "where name like '%value%'"
            match = re.search(r'where (\w+) like "(.*)"', nlp_input)
            if match:
                column, pattern = match.groups()
                query = f"SELECT * FROM `{table_name}` WHERE `{column}` LIKE '%{pattern}%';"
                execute_query(connection, query)
        else:
            match = re.search(r'where (\w+) (>=|<=|>|<|=) (".*"|\d+)', nlp_input)
            if match:
                column, operator, value = match.groups()
                # Remove the quotes if it's a string value
                value = value.strip('"') if value.startswith('"') else value
                if not value.isnumeric():
                    value = f"'{value}'"
                query = f"SELECT * FROM `{table_name}` WHERE `{column}` {operator} {value};"
                execute_query(connection, query)
            else:
                print("Fail to match.")
    
    # Common queries for comma-separated columns, "get col1, col2, col3"
    elif any(word in lemmatized_input for word in ['get', 'return', 'retrieve', 'output']):
        match = re.search(r'(get|return|retrieve|output) (.+)', nlp_input)
        if match:
            _, columns = match.groups()
            columns = ", ".join([f"`{col.strip()}`" for col in columns.split(",")])
            query = f"SELECT {columns} FROM `{table_name}`;"
            execute_query(connection, query)

    else:
        print("Could not match the input pattern.")

