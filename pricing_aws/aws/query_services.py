import json
from constants import AVAILABLE_OFFERS_MAP
from pathlib import Path
from query_api import get_price_list, get_services
from typing import Literal

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

_INFO_TYPES = Literal['service_list', 'pricing_data']


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
    offer = get_service_code(service_code, False, service_code)

    try:
        attributes = json_data[offer]
        for index, attr in enumerate(attributes):
            if attribute.lower() == attr.lower():
                return attributes[index]
    except KeyError:
        pass

    available_attributes = ', '.join(attributes)
    raise ValueError(f'Attribute name {attribute} not available for service {service_code}\nAvailable Attributes:\n\n{available_attributes}')


# print(get_service_code('services.json', False, 'amazons3'))
print(verify_attribute('AmazonEC2', 'voltype', 'us-east-1'))
# get_file_data('AmazonS3', 'us-gov-west-1')
# print(get_service_code('AmazonEC2', 'us-gov-west-1', False))
