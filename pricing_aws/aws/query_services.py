import json
from constants import AVAILABLE_OFFERS_MAP
from pathlib import Path
from typing import Literal
import datetime
import requests
import boto3

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

_INFO_TYPES = Literal['service_list', 'pricing_data']
pricing = boto3.client('pricing')


def get_file_data(service_code, region, info_type: _INFO_TYPES):
    """
    Get file contents and return information
    """
    if info_type == 'pricing_data':
        service_file = f'{service_code}-{region}.json'
    else:
        service_file = f'services-{region}.json'
    path_file = Path(f'{service_file}')
    if not path_file.is_file():
        if info_type == 'pricing_data':
            get_price_list(service_code, region, replace_file=True)
        else:
            get_services(f'services-{region}.json', replace_file=True)
    with open(service_file, 'r') as sf:
        return json.load(sf)
    

def get_price_list(service_name, region, replace_file=False, pricing_filename=None):
    # type: (str, str, bool, str) -> None
    """
    Get the URL for the price list
    """
    if not replace_file:
        pass

    if pricing_filename == None:
        pricing_filename = f'{service_name}-{region}.json'
    price_list = pricing.list_price_lists(
        ServiceCode=service_name,
        RegionCode=region,
        EffectiveDate=datetime.datetime.today(),
        CurrencyCode='USD'
    )
    if price_list['PriceLists'] == []:
        raise ValueError(f'No price list found for service {service_name} in region {region}')
    file_url = pricing.get_price_list_file_url(
        PriceListArn=price_list['PriceLists'][0]['PriceListArn'],
        FileFormat='json'
    ).get('Url')
    with open(pricing_filename, 'wb') as pfw:
        for chunk in requests.get(file_url, stream=True).iter_content(chunk_size=128):
            pfw.write(chunk)
    

def get_services(output_filename='services.json', replace_file=False):
    # type: (str, bool) -> None
    """
    Fetches AWS services and their attribute names, then saves the data to a JSON file.

    :param output_filename: The name of the output JSON file.
    :type output_filename: str
    """
    all_services = {}
    if not replace_file:
        pass

    services = pricing.describe_services()
    while True:
        for service in services['Services']:
            all_services[service['ServiceCode']] = service['AttributeNames']
        if 'NextToken' not in services:
            break
        services = pricing.describe_services(NextToken=services['NextToken'])

    with open(output_filename, 'w') as json_file:
        json.dump(all_services, json_file, indent=4)


def get_service_code(type, region, return_all=True):
    # type: (str, str, bool) -> str
    """
    Get service information from the API and return all data or only portions of the data

    :param type: if return_all is False, provide the specific service to return info for
    :type service_file: str

    :param region: region the service(s) will be in
    :type service_file: str

    :param return_all: Whether to return all services or a specific service
    :type service_file: bool
    """

    if type.lower() in AVAILABLE_OFFERS_MAP:
        # return full name matched with short name
        return AVAILABLE_OFFERS_MAP[type]
        
    json_data = get_file_data(type, region, info_type='service_list')
    # user lowercase for case insensitive checking
    services_lowercase = []
    services = []
    for service_data in json_data:
        services.append(service_data)
        services_lowercase.append(service_data.lower())
    if return_all:
        return services

    print(services_lowercase)
    if type.lower() not in services_lowercase:
        raise ValueError('Unknown offer name: {}'.format(type))
    
    # get index of match in list
    idx = services_lowercase.index(type.lower())
    # return matching correct-case name
    return services[idx]


# print(get_service_code('services.json', False, 'amazons3'))
# get_file_data('AmazonS3', 'us-gov-west-1')
# print(get_service_code('AmazonEC2', 'us-gov-west-1', False))
