import json
from constants import AVAILABLE_OFFERS_MAP

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def get_file_data(service_file):
    """
    Get file contents and return information
    """
    with open(service_file, 'r') as sf:
        return json.load(sf)


def get_service_code(service_file, return_all=True, type=None):
    # type: (str, bool, str) -> str
    """
    Get service information from the API and return all data or only portions of the data

    :param service_file: Location of service file containing the services list
    :type service_file: str

    :param return_all: Whether to return all services or a specific service
    :type service_file: bool

    :param type: if return_all is False, provide the specific service to return info for
    :type service_file: str
    """

    json_data = get_file_data(service_file)
    # user lowercase for case insensitive checking
    services_lowercase = []
    services = []
    for service_data in json_data:
        services.append(service_data)
        services_lowercase.append(service_data.lower())
    if return_all:
        return services

    if type.lower() not in services_lowercase:
        if type not in AVAILABLE_OFFERS_MAP:
            raise ValueError('Unknown offer name: {}'.format(type))
        # return full name matched with short name
        return AVAILABLE_OFFERS_MAP[type]
    # get index of match in list
    idx = services_lowercase.index(type.lower())
    # return matching correct-case name
    return services[idx]


def verify_attribute(service_file, type, attribute):
    # type: (str, str, str) -> str
    """
    Verify an attribute is used in a service code and if so, return the correct casing
    
    :param service_file: Location of service file containing the services list
    :type service_file: str

    :param type: The service code the attribute is used for
    :type service_file: str

    :param attribute: The attribute name to verify
    :type service_file: str
    """

    json_data = get_file_data(service_file)
    offer = get_service_code(service_file, False, type)
    attributes = json_data[offer]

    for idx, attr in enumerate(attributes):
        if attribute.lower() == attr.lower():
            return attributes[idx]
    raise ValueError(f'Attribute name {attribute} not available for service {type}\nAvailable Attributes:\n\n{str(attributes)}')

# print(get_service_code('services.json', False, 'amazons3'))
print(verify_attribute('services.json', 'ec2', 'volumetype'))
