import pandas as pd
import search_skus

doc = pd.read_excel("test.xlsx", keep_default_na=False)
# lowercase the column names
doc.rename(columns=lambda s: s.lower(), inplace=True)
print(doc)

sku = search_skus.main()

all_costs = {}

# iterate the rows and update cost
for index, name in doc.iterrows():
    attrs = name.to_dict()
    # need to get the heading
    cost = sku.search_skus(database='products', attributes=attrs)
    all_costs[index] = cost
# print(doc)

print(all_costs)

# doc['cost'] = all_costs

# # output to excel
# doc.to_excel('a.xlsx', sheet_name='hello')
