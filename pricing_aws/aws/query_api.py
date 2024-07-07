from typing import Dict, Set
import boto3
import json
from query_services import get_file_data, get_service_code

pricing = boto3.client('pricing')


def get_products(service_name, filters=[]):
    # type: (str, list[Dict[str, str]]) -> Set[str]
    """
    Retrieves product information from AWS Pricing API based on the specified service name and filters.

    :param service_name: The AWS service code for which product information is requested.
    :type service_name: str

    :param filters: Additional filters to narrow down the search.
    :type filters: list of dict

    :return: None
    """
    all_products = []  # List to store retrieved product information

    paginator = pricing.get_paginator('get_products')

    # Merge default and user-defined filters when making the API call
    products_iterator = paginator.paginate(
        ServiceCode=service_name,
        Filters=filters
    )

    # Extract product information from the API response and extend the product list
    for pi in products_iterator:
        all_products.extend(json.loads(prod)
                            for prod in pi.get('PriceList', []))

    # Save the retrieved product information to a JSON file
    with open('ec2.json', 'w') as bw:
        json.dump(all_products, bw, indent=4)

    return all_products


def build_filter(attributes):
    # type: (Dict[str,str]) -> list[Dict[str,str]]
    """
    Take list of attributes and return in correct filter format used by the API

    :param attributes: Attributes used for searching data
    :type attributes: list[Dict[str,str]]
    """
    formatted_filter = []
    for key in attributes:
        # Check if the item matches all the filter conditions
        new_key = verify_attribute(key)
        template = {'Type': 'TERM_MATCH',
                    'Field': new_key, 'Value': attributes.get(key)}
        formatted_filter.append(template)
        

    return formatted_filter


def verify_attribute(service_code, attribute, region):
    # type: (str, str, str) -> str
    """
    Verify an attribute is used in a service code and if so, return the correct casing
    
    :param service_code: The service code the attribute is used for
    :type service_code: str

    :param attribute: The attribute name to verify
    :type attribute: str

    :param region: The region for which service data is requested
    :type region: str

    :return: Correct casing of the attribute if found
    :rtype: str
    """
    json_data = get_file_data(service_code, region, 'service_list')
    offer = get_service_code(service_code, region, False)

    try:
        attributes = json_data[offer]
        for index, attr in enumerate(attributes):
            if attribute.lower() == attr.lower():
                return attributes[index]
    except KeyError:
        pass

    available_attributes = ', '.join(attributes)
    raise ValueError(f'Attribute name {attribute} not available for service {service_code}\nAvailable Attributes:\n\n{available_attributes}')


Filters = [
    {'Type': 'TERM_MATCH','Field': 'tenancy','Value': 'Shared'},
    {'Type': 'TERM_MATCH','Field': 'licensemodel','Value': 'No License required'},
    {'Type': 'TERM_MATCH','Field': 'instanceType','Value': 'm5.large'},
    {'Type': 'TERM_MATCH','Field': 'regionCode','Value': 'us-east-1'},
    {'Type': 'TERM_MATCH','Field': 'capacitystatus','Value': 'Used'},
    {'Type': 'TERM_MATCH','Field': 'productFamily','Value': 'Compute Instance'},
    {'Type': 'TERM_MATCH','Field': 'operatingSystem','Value': 'RHEL'},
    {'Type': 'TERM_MATCH','Field': 'preInstalledSw','Value': 'NA'},
]

Filters2 = [
    {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'IP Address'}
]

# get_products('AmazonEC2', Filters)

# service = 'AmazonRDS'
# get_price_list(service)
# with open(f'{service}.json', 'r') as js:
#     data = json.load(js)

# for d in data['terms']:
#     print(d)

# print(verify_attribute('AmazonEC2', 'voltype', 'us-east-1'))