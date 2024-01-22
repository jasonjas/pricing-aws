from typing import Literal, Dict
import json

_TERMS_TYPES = Literal["OnDemand", "Reserved"]

# create a lambda to loop through the keys
def v(d): return list(d.values())[0]

def get_price(pricing_data, terms_type: _TERMS_TYPES = 'OnDemand'):
    # type: (Dict, str) -> float
    """
    Return hourly rate for specific sku
    """
    if terms_type not in ['OnDemand', 'Reserved']:
        raise ValueError(f'terms_type must be one of OnDemand or Reserved')

    od_terms = json.loads(pricing_data.get('terms')).get(terms_type)
    if terms_type == 'OnDemand':
        # Loop 2 keys down to get the price
        hourly_cost = v(v(od_terms)['priceDimensions'])['pricePerUnit']['USD']

    if terms_type == 'Reserved':
        hourly_cost = get_terms(od_terms)

    # hourly_cost = v(v(v(od_terms))['priceDimensions'])['pricePerUnit']['USD']
    return hourly_cost


def get_terms(terms_data, years=1, offering_class='convertible', purchase_option='No Upfront'):
    # type: (Dict, int, str, str) -> float
    """

    """
    for idx, val in enumerate(terms_data):
        option_data = terms_data[val].get('termAttributes')
        # return values for 1 year, convertible, no-upfront payment
        if option_data['LeaseContractLength'] == f'{years}yr' and option_data['OfferingClass'] == offering_class and option_data['PurchaseOption'] == purchase_option:
            # loop 3 keys down on the index to get the price
            hourly_cost = v(v(v(terms_data)[idx])[0])[
                0]['pricePerUnit']['USD']
            
    return hourly_cost

# def query_test():
#     with open('ec2.json', 'r') as ro:
#         data = json.load(ro)

#     od_terms = data[0].get('terms').get('Reserved')
#     def v(d): return list(d.values())
#     # print(v(v(od_terms)['priceDimensions'])['pricePerUnit']['USD'])

#     for idx, val in enumerate(od_terms):
#         option_data = od_terms[val].get('termAttributes')
#         if option_data['LeaseContractLength'] == '1yr' and option_data['OfferingClass'] == 'convertible' and option_data['PurchaseOption'] == 'No Upfront':
#             print(v(v(v(od_terms)[idx])[0])[0]['pricePerUnit']['USD'])
            # print(json.dumps(od_terms.get(val), indent=4))

    # print(json.dumps(v(v(od_terms)['priceDimensions'])['pricePerUnit']['USD'], indent=4))

    # print(descend_json(od_terms['DZBZFBHFHVERPMQZ'], 1))
    # print(hourly_cost)


query_test()
