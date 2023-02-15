from typing import Any, Dict, List, Optional, Set, Type
import logging
import query_db
from constants import (
    REGION_SHORTS,
    RESOURCE_TYPES_MAPPING
)

OFFER_CLASS_MAP = {}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def implements(offer_name):
    """Decorator to keep track of offer-specific class implementations."""
    def wrapper(cls):
        OFFER_CLASS_MAP[offer_name] = cls
        return cls
    return wrapper


def get_offer_class(offer_name):  # type: (str) -> Type[main]
    return OFFER_CLASS_MAP.get(offer_name, main)


class main:
    def __init__(self) -> None:
        self.default_region = 'us-east-1'
        self.default_resource_type = 'vm'

    # type: (str, Dict[str, str]) -> Set[str]
    def search_skus(self, database, attributes):
        """Search for all SKUs matching the given attributes.

        Note that attributes given in pythonic snake_case notation will
        automatically be converted to camelCase to match AWS pricing data
        convention.

        :return: a set of matching SKUs
        """
        attributes = self._pythonify_attributes(attributes)
        query = query_db.build_query(database, attributes, 'sku')
        print(query)
        # col_names = query_db.get_column_names(database)
        result = query_db.query_products(query)
        return result

    def _pythonify_attributes(self, attributes):
        # type: (Dict[str, str]) -> Dict[str, str]
        result = {}
        prefix = 'attributes_'
        for attr_name in attributes:
            attr_value = attributes[attr_name]
            if attr_name == 'type':
                attr_name = 'productFamily'
                attr_value = self._normalize_resource_type(attr_value)
            elif attr_name == 'region':
                attr_name = f'{prefix}regionCode'
            elif attr_name != "index" and attr_name != "sku" and attr_name != "productFamily":
                # add 'attributes_' before the column name
                attr_name = f'{prefix}{attr_name}'
                attr_name = attr_name[0].lower() + attr_name[1:]

            result[attr_name] = attr_value
        return result

    def _normalize_region(self, region):  # type: (Optional[str]) -> str
        region = region or self.default_region
        if not region:
            raise ValueError("No region is set.")

        if region in REGION_SHORTS:  # Use long-name to match pricing API
            region = REGION_SHORTS[region]
        return region

    # type: (Optional[str]) -> str
    def _normalize_resource_type(self, type: str):
        type = type or self.default_resource_type

        if not type:
            raise ValueError("No resource type is set.")

        if type in RESOURCE_TYPES_MAPPING:  # Use product family to match pricing API
            type = RESOURCE_TYPES_MAPPING[type]
        return type

    # type: (str, Dict[str, str]) -> Dict[str, str]
    def verify_attributes(self, product_family, attributes):
        # Loop through attributes and verify required ones exist.
        # If not in attributes, add them
        defaults = get_offer_class(product_family)
        


