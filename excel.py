import pandas as pd
import search_skus
from constants import HOURS_IN_MONTH

doc = pd.read_excel("test.xlsx", keep_default_na=False, sheet_name=None)
sku = search_skus.main()

for sheet in doc:
    # lowercase the column names
    doc[sheet].rename(columns=lambda s: s.lower(), inplace=True)

    all_costs = {}

    # iterate the rows and update cost
    for index, name in doc[sheet].iterrows():
        attrs = name.to_dict()
        # need to get the heading
        cost = sku.get_pricing(attributes=attrs)
        all_costs[index] = float(cost) * HOURS_IN_MONTH
    doc[sheet]['monthly_cost'] = all_costs

    # output to excel

writer = pd.ExcelWriter('complete.xlsx', engine='openpyxl')
for sheet, frame in doc.items():
    frame.to_excel(writer, sheet_name=sheet, index=False)
writer.close()
