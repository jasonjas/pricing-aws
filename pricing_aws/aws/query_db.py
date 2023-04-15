import sqlite3
import pandas as pd
from typing import Dict
from constants import PRODUCTS_DATABASE_FILE_NAME

def populate_products_database(table_name, json_index='products', src_file_path='index-full.json', dest_file_path='products.db'):
    # type: (str, str, str, str) -> None
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
    prods.to_sql(table_name, con, if_exists='replace')
    con.close()


def descend_json(x, depth):
    # type (Dict, int) -> any
    """Iterate through a dict-like object and return the data specified in the depth value
    """
    for i in range(depth):
        x = next(iter(x.values()))

    return x


def populate_terms_db(table_name, json_index='terms', src_file_path='index-full.json', dest_file_path='terms.db'):
    # type: (str, str, str, str) -> None
    """Create database from pricing API index data

    args:
        table_name: name of table to create in the db file
        json_index: top-level index of json to output, ex. 'products' or 'terms'
        src_file_path: relative or full file path to source index json file
        dest_file_path: relative or full file path to database that is wanted to be created/replaced

    return: saves the output to a database file on the filesystem
    """
    table_data = {}
    jsonfile = pd.read_json(src_file_path)  # , orient='index'
    odterms = jsonfile[json_index]['OnDemand']

    for sku in odterms:
        data = descend_json(odterms[sku], 1)
        price_data = descend_json(data['priceDimensions'], 1)
        table_data[sku] = {'sku': sku, 'description': price_data['description'],
                           'unit': price_data['unit'], 'cost': price_data['pricePerUnit']['USD']}
    # t_to_j = json.loads(json.dumps(table_data))
    jn = pd.json_normalize(table_data.values())
    con = sqlite3.connect(dest_file_path)
    jn.to_sql(table_name, con, if_exists='replace')
    con.close()


def build_query(table, values, columns='*'):
    # type: (str, Dict[str, str], str) -> str
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
        # leave out any fields left intentionally null
        if values[col] == '':
            continue
        if where_clause_values != '':
            where_clause_values += " AND "
        where_clause_values += f"{col} == '{values[col]}'"
    query_string = f"{db_string} WHERE {where_clause_values}"

    return query_string


def query_db(query_string, db_file_name):  # type: (str, str) -> tuple
    """Query database using the query string provided

    args:
        query_string: database query string

    return: results of the query
    """
    cur = _create_connection(db_file=db_file_name)
    query_results = cur.execute(query_string)
    results = query_results.fetchall()
    cur.close()
    return results[0]


def get_column_names(table_name):  # type: (str) -> list
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


def _create_connection(db_file):  # type: (str) -> sqlite3.Cursor
    """Create a sqlite connection to a database file

    args:
        db_file: relative or full file path to database

    return: sqlite3 cursor object
    """
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    return cur


def get_table_info(db_file, table_name='products'):
    # type (str, str) -> sqlite3.Cursor
    """Get sqlite pragma table info in the database

    args:
        db_file: relative or full file path to database file

    return: sqlite3 cursor object
    """
    cur = _create_connection()
    tables = cur.execute(f"PRAGMA table_info({table_name});")
    cur.close()
    return tables

# populate_products_database('ec2', dest_file_path='products.db')
# populate_terms_db('ec2')