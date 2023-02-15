import pandas as pd
import sqlite3

jsonfile = pd.read_json('index-full.json')
products = jsonfile['products']

prods = pd.json_normalize(products.values)
# rename columns
prods.rename(columns=lambda s: s.lower().replace('attributes.', 'attributes_'), inplace=True)
con = sqlite3.connect("products.db")
prods.to_sql('products', con)

# terms = jsonfile['terms']['OnDemand']
# get terms
# terms[sku]

# print(json.loads(terms.values))
prods = pd.json_normalize(products.values)
# rename columns
prods.rename(columns=lambda s: s.lower().replace('attributes.', 'attributes_'), inplace=True)
con = sqlite3.connect("products.db")
prods.to_sql('products', con)
# columns = []
# for pc in prods.columns:
#     new_col_name = pc.replace('attributes.', 'attributes_')
#     if 'attributes.' in new_col_name:
#         prods.rename(columns={pc: new_col_name}, inplace=True)
#     columns.append(new_col_name)
# cols = ','.join(columns)

# print(cols)




# cur = con.cursor()
# print(con.execute('SELECT * FROM products'))