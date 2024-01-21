from typing import Literal, Dict
import json

_TERMS_TYPES = Literal["OnDemand", "Reserved"]


def descend_json(x, depth):
    # type (Dict, int) -> any
    """Iterate through a dict-like object and return the data specified in the depth value
    """
    for i in range(depth):
        x = next(iter(x.values()))

    return x


def get_price(pricing_data, sku, terms_type: _TERMS_TYPES = 'OnDemand'):
    # type: (Dict, str, str) -> float
    if terms_type not in ['OnDemand', 'Reserved']:
        raise ValueError(f'terms_type must be one of OnDemand or Reserved')

    od_terms = json.loads(pricing_data.get('terms')).get(terms_type)
    # create a lambda to loop through the keys
    def v(d): return list(d.values())[0]

    if terms_type == 'OnDemand':
        # Loop 2 keys down to get the price
        hourly_cost = v(v(od_terms)['priceDimensions'])['pricePerUnit']['USD']

    if terms_type == 'Reserved':
        for idx, val in enumerate(od_terms):
            option_data = od_terms[val].get('termAttributes')
            # return values for 1 year, convertible, no-upfront payment
            if option_data['LeaseContractLength'] == '1yr' and option_data['OfferingClass'] == 'convertible' and option_data['PurchaseOption'] == 'No Upfront':
                # loop 3 keys down on the index to get the price
                hourly_cost = v(v(v(od_terms)[idx])[0])[
                    0]['pricePerUnit']['USD']

    # hourly_cost = v(v(v(od_terms))['priceDimensions'])['pricePerUnit']['USD']
    return hourly_cost


def query_test():
    with open('ec2.json', 'r') as ro:
        data = json.load(ro)

    od_terms = data[0].get('terms').get('Reserved')
    def v(d): return list(d.values())
    # print(v(v(od_terms)['priceDimensions'])['pricePerUnit']['USD'])

    for idx, val in enumerate(od_terms):
        option_data = od_terms[val].get('termAttributes')
        if option_data['LeaseContractLength'] == '1yr' and option_data['OfferingClass'] == 'convertible' and option_data['PurchaseOption'] == 'No Upfront':
            print(v(v(v(od_terms)[idx])[0])[0]['pricePerUnit']['USD'])
            # print(json.dumps(od_terms.get(val), indent=4))

    # print(json.dumps(v(v(od_terms)['priceDimensions'])['pricePerUnit']['USD'], indent=4))

    # print(descend_json(od_terms['DZBZFBHFHVERPMQZ'], 1))
    # print(hourly_cost)


query_test()
