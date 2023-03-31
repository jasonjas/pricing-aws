"""Default attributes for each offer class
These also designate the *required* attributes
"""

from typing import Dict

DEFAULT_FUNCTION_MAP = {}


def implements(offer_name):
    """Decorator to keep track of offer-specific default attributes."""
    def wrapper(cls):
        DEFAULT_FUNCTION_MAP[offer_name] = cls
        return cls
    return wrapper


def get_defaults(offer_name):  # type: (str) -> str
    return DEFAULT_FUNCTION_MAP.get(offer_name)


@implements("ec2_default_attributes")
def ec2_default_attributes(): # type: () -> Dict[str,str]
    return {
        'attributes_operatingsystem': 'RHEL',
        'attributes_tenancy': 'Shared',
        'attributes_licensemodel': 'No License required',
        'attributes_preinstalledsw': 'NA',
        'attributes_capacitystatus': 'Used',
        'attributes_marketoption': 'OnDemand'
    }
