from typing import Dict
import boto3
import json
import datetime

pricing = boto3.client('pricing')

def get_services(output_filename='services.json'):
    # type: (str) -> None
    all_services = {}
    services = pricing.describe_services()
    while 'NextToken' in services.keys():
        services = pricing.describe_services(NextToken=services['NextToken'])
        for i in services['Services']:
            print(i)
            all_services.update({i['ServiceCode']: i['AttributeNames']})

    with open(output_filename, 'w') as aj:
        json.dump(all_services, aj, indent=4)


def get_price_list(service_name, region='us-east-1'):
    # type: (str, str) -> None
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

def get_products(service_name, filter):
    all_products = []
    paginator = pricing.get_paginator('get_products')
    products_iterator = paginator.paginate(
        ServiceCode=service_name,
        # Filters=filter
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'tenancy',
                'Value': 'Shared'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'licensemodel',
                'Value': 'No License required'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceType',
                'Value': 'm5.large'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'regionCode',
                'Value': 'us-east-1'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'capacitystatus',
                'Value': 'Used'
            },
        ]
    )
    for pi in products_iterator:
        for prod in pi['PriceList']:
            all_products.append(json.loads(prod))
            
    with open('b.json', 'w') as bw:
        json.dump(all_products, bw, indent=4)

# get_price_list('AmazonEC2')
# get_products('AmazonEC2')
        
get_services()