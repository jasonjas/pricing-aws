import sqlite3
import pandas as pd
from typing import Dict
from constants import DATABASE_FILE_NAME

###
# Get information to query and build the query here
###

# build query
# take in stuff

# con = sqlite3.connect("products.db")
# cur = con.cursor()
# res = cur.execute("SELECT * from products WHERE sku == 'DSF55NK4A6B6FWMD'")
#         # "SELECT attributes_group,sku from products WHERE attributes_group != ''")
#         #"SELECT * FROM products WHERE attributes_location == 'US East (N. Virginia)' AND attributes_instanceType == 'r5d.12xlarge'"):

# for i in res.fetchall():
#     print(i)
# cur.close()


# type: (str, str, str, str) -> None
def populate_database(table_name, json_index, src_file_path='index-full.json', dest_file_path='data.db'):
    """Create database from pricing API index data

    args:
        table_name: name of table to create in the db file
        json_index: top-level index of json to output, ex. 'products' or 'terms'
        src_file_path: relative or full file path to source index json file
        dest_file_path: relative or full file path to database that is wanted to be created/replaced

    return: saves the output to a database file on the filesystem
    """
    jsonfile = pd.read_json(src_file_path)
    products = jsonfile[json_index]

    prods = pd.json_normalize(products.values)
    # rename columns and set to lowercase
    prods.rename(columns=lambda s: s.lower().replace(
        'attributes.', 'attributes_'), inplace=True)
    con = sqlite3.connect(dest_file_path)
    prods.to_sql(table_name, con)


def build_query(table, values, columns='*'): # type: (str, Dict[str, str], str) -> str
    """Create the query string used to query the database

    args:
        table: name of table to query in the database
        values: dictionary of tables and search values to query the database
        columns: the column(s) to return data for

    return: the full query string
    """
    db_string = f"SELECT {columns} FROM {table}"
    where_clause_values = ''
    for col in values:
        if where_clause_values != '':
            where_clause_values += " AND "
        where_clause_values += f"{col} == '{values[col]}'"
    query_string = f"{db_string} WHERE {where_clause_values}"

    return query_string


def query_products(query_string): # type: (str) -> any
    """Query database using the query string provided

    args:
        query_string: database query string

    return: results of the query
    """
    cur = _create_connection()
    query_results = cur.execute(query_string)
    results = query_results.fetchall()
    cur.close()
    return results


def get_column_names(table_name): # type: (str) -> list
    """Retrieve the column names in the specified table

    args:
        table_name: name of the table to get columns from

    return: list of column names
    """
    cur = _create_connection()
    cur.execute(f"select * from {table_name} limit 1")
    col_names = [i[0] for i in cur.description]
    cur.close()
    return col_names


def _create_connection(db_file=DATABASE_FILE_NAME): # type: (str) -> sqlite3.Cursor
    """Create a sqlite connection to a database file

    args:
        db_file: relative or full file path to database

    return: sqlite3 cursor object
    """
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    return cur


def get_table_info(db_file=DATABASE_FILE_NAME, table_name='products'): # type (str, str) -> sqlite3.Cursor
    """Get sqlite pragma table info in the database

    args:
        db_file: relative or full file path to database file

    return: sqlite3 cursor object
    """
    cur = _create_connection()
    tables = cur.execute(f"PRAGMA table_info({table_name});")
    cur.close()
    return tables
