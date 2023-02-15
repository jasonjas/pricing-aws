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
def populate_database(database, json_index, src_file_path='index-full.json', dest_file_path='data.db'):
    jsonfile = pd.read_json(src_file_path)
    products = jsonfile[json_index]

    prods = pd.json_normalize(products.values)
    # rename columns and set to lowercase
    prods.rename(columns=lambda s: s.lower().replace(
        'attributes.', 'attributes_'), inplace=True)
    con = sqlite3.connect(dest_file_path)
    prods.to_sql(database, con)


def build_query(database: str, values: Dict[str, str], columns='*'):
    db_string = f"SELECT {columns} FROM {database}"
    where_clause_values = ''
    for col in values:
        if where_clause_values != '':
            where_clause_values += " AND "
        where_clause_values += f"{col} == '{values[col]}'"
    query_string = f"{db_string} WHERE {where_clause_values}"

    return query_string


def query_products(query_string: str):
    cur = _create_connection()
    query_results = cur.execute(query_string)
    results = query_results.fetchall()
    cur.close()
    return results


def get_column_names(database: str):
    cur = _create_connection()
    cur.execute(f"select * from {database} limit 1")
    col_names = [i[0] for i in cur.description]
    cur.close()
    return col_names


def _create_connection(db_file=DATABASE_FILE_NAME):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    return cur


def get_tables(db_file=DATABASE_FILE_NAME):
    cur = _create_connection()
    tables = cur.execute("PRAGMA table_info(products);")
    print(tables.fetchall())
    cur.close()
    return tables
