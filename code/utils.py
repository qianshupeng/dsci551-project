# utils.py
# helper functions other than existing modules

import os

def is_valid_file(file_path):
    return os.path.isfile(file_path) and file_path.endswith('.csv')

def get_table_name(file_path):
    """Generate a table name from the CSV file name."""
    return os.path.splitext(os.path.basename(file_path))[0]