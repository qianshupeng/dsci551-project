# utils.py
# Helper functions besides existing modules

import os
import pandas as pd

def is_valid_file(file_path):
    """Check if the file path is valid and if the file is in CSV format."""
    return os.path.isfile(file_path) and file_path.endswith('.csv')

def get_table_name(file_path):
    """Generate a table name from the CSV file name."""
    return os.path.splitext(os.path.basename(file_path))[0]

def infer_column_types(df):
    """Infer SQL data types for each column in a DataFrame."""
    inferred_types = []
    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]):
            inferred_types.append("INT")
        elif pd.api.types.is_float_dtype(df[col]):
            inferred_types.append("FLOAT")
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            inferred_types.append("DATETIME")
        else:
            inferred_types.append("VARCHAR(255)")
    return inferred_types