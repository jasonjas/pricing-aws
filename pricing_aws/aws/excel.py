import pandas as pd
import search_skus
from constants import HOURS_IN_MONTH

def process_excel_doc(input_file_name, output_file_name):
    doc = pd.read_excel(input_file_name, keep_default_na=False, sheet_name=None)
    sku = search_skus.main()

    for sheet in doc:
        # lowercase the column names
        doc[sheet].rename(columns=lambda s: s.lower(), inplace=True)

        all_costs = {}

        # iterate the rows and update cost
        for index, name in doc[sheet].iterrows():
            attrs = name.to_dict()
            multiplier = HOURS_IN_MONTH
            if 'storage-size-gb' in attrs.keys():
                multiplier = attrs['storage-size-gb']
                attrs.pop('storage-size-gb', None)
            cost = sku.get_pricing(attributes=attrs)
            all_costs[index] = float(cost) * float(multiplier)
        doc[sheet]['monthly_cost'] = all_costs

        # output to excel

    writer = pd.ExcelWriter(output_file_name, engine='openpyxl')
    for sheet, frame in doc.items():
        frame.to_excel(writer, sheet_name=sheet, index=False)
    writer.close()
