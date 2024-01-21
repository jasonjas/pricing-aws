from typing import Dict, Set
import boto3
import json
import datetime

pricing = boto3.client('pricing')


def get_services(output_filename='services.json'):
    # type: (str) -> None
    """
    Fetches AWS services and their attribute names, then saves the data to a JSON file.

    :param output_filename: The name of the output JSON file.
    :type output_filename: str
    """
    all_services = {}

    services = pricing.describe_services()
    while True:
        for service in services['Services']:
            all_services[service['ServiceCode']] = service['AttributeNames']
        if 'NextToken' not in services:
            break
        services = pricing.describe_services(NextToken=services['NextToken'])

    with open(output_filename, 'w') as json_file:
        json.dump(all_services, json_file, indent=4)

def get_price_list(service_name, region='us-east-1'):
    # type: (str, str) -> None
    """
    Get the URL for the price list
    """
    price_list = pricing.list_price_lists(
        ServiceCode=service_name,
        RegionCode=region,
        EffectiveDate=datetime.datetime.today(),
        CurrencyCode='USD'
    )
    print(json.dumps(price_list, indent=4))
    file_url = pricing.get_price_list_file_url(
        PriceListArn=price_list['PriceLists'][0]['PriceListArn'],
        FileFormat='json'
    )
    print(file_url)


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
        template = {'Type': 'TERM_MATCH',
                    'Field': key, 'Value': attributes.get(key)}
        formatted_filter.append(template)
        # Check if the item matches all the filter conditions

    return formatted_filter


Filters = [
    {'Type': 'TERM_MATCH','Field': 'tenancy','Value': 'Shared'},
    {'Type': 'TERM_MATCH','Field': 'licensemodel','Value': 'No License required'},
    {'Type': 'TERM_MATCH','Field': 'instanceType','Value': 'm5.large'},
    {'Type': 'TERM_MATCH','Field': 'regionCode','Value': 'us-east-1'},
    {'Type': 'TERM_MATCH','Field': 'capacitystatus','Value': 'Used'},
    {'Type': 'TERM_MATCH','Field': 'productFamily','Value': 'Dedicated Host'},
    {'Type': 'TERM_MATCH','Field': 'operatingSystem','Value': 'RHEL'},
]

Filters2 = [
    {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'IP Address'}
]

# get_price_list('AmazonEC2')
get_products('AmazonEC2', Filters2)
