from typing import Any, Dict, List, Optional, Set, Type
import logging
import query_db
import defaults
from constants import (
    REGION_SHORTS,
    RESOURCE_TYPES_MAPPING,
    PRODUCTS_DATABASE_FILE_NAME,
    TERMS_DATABASE_FILE_NAME,
    DB_NAME_MAPPING
)

OFFER_CLASS_MAP = {}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class main:
    def __init__(self) -> None:
        self.default_region = 'us-east-1'
        self.default_resource_type = 'ec2'

    # type: (str, str, Dict[str, str]) -> Set[str]
    def search_products(self, database, attributes, product_type):
        """Search for all products matching the given attributes.

        args:
            database: name of database file containing the data to search
            attributes: dictionary of attributes to search for

        return: a set of matching SKUs
        """
        attributes = self._pythonify_attributes(attributes)
        all_attrs = self.check_defaults(attributes, product_type)
        query = query_db.build_query(database, all_attrs, 'sku')
        result = query_db.query_db(query, db_file_name=PRODUCTS_DATABASE_FILE_NAME)
        return result
    

    # type: (str, str, str, Dict[str, str]) -> Set[str]
    def get_pricing(self, attributes):
        """Search for all SKUs matching the given attributes.

        args:
            database: name of database file containing the data to search
            attributes: dictionary of attributes to search for

        return: pricing information
        """
        terms_attrs = {}
        product_type = attributes['type']
        database_name = DB_NAME_MAPPING[product_type]
        attributes = self._pythonify_attributes(attributes)
        all_attrs = self.check_defaults(attributes, product_type)
        sku = self.search_products(database_name, all_attrs, product_type)
        if len(sku) != 1:
            raise ValueError(f"Only 1 sku can be used to query the DB, received {len(sku)}")
        terms_attrs['sku'] = sku[0]
        query = query_db.build_query(database_name, terms_attrs, 'cost')
        result = query_db.query_db(query, db_file_name=TERMS_DATABASE_FILE_NAME)
        return result[0]


    def check_defaults(self, attributes, product_type): # type: (Dict[str, str], str) -> Dict[str, str]
        """Check defined attributes and add any default attributes that are required but do not exist in the request

        return: Dictionary of attributes and their values
        """
        default_attrs = {}
        if 'productfamily' in attributes.keys():
            productFamily = self._normalize_resource_type(attributes['productfamily'])
            # in a very complicated way, get the original type from the resource_types_Mapping dictionary
            # type = list(RESOURCE_TYPES_MAPPING.keys())[list(RESOURCE_TYPES_MAPPING.values()).index(productFamily)]
            default_attrs = defaults.get_defaults(f'{product_type}_default_attributes')()
        for i in default_attrs.keys():
            if i not in attributes.keys():
                attributes[i] = default_attrs[i]
        return attributes

    def _pythonify_attributes(self, attributes):
        # type: (Dict[str, str]) -> Dict[str, str]
        """Return attributes to match what is loaded/created in the database

        return: Dictionary of attributes and their values
        """
        result = {}
        prefix = 'attributes_'
        for attr_name in attributes:
            attr_value = attributes[attr_name]
            if attr_name == 'type':
                attr_name = 'productfamily'
                attr_value = self._normalize_resource_type(attr_value)
            elif attr_name == 'region':
                attr_name = f'{prefix}regionCode'
            elif attr_name.startswith(prefix):
                attr_name = attr_name.lower()
            elif attr_name == 'storage-size-gb' and attr_value == 'Storage':
                # storage-size is only used for calculating the costs
                attributes.pop('storage-size-gb')
                continue
            elif attr_name != "index" and attr_name != "sku" and attr_name != "productfamily":
                # add 'attributes_' before the column name
                attr_name = f'{prefix}{attr_name}'
                attr_name = attr_name[0].lower() + attr_name[1:]

            result[attr_name] = attr_value
        return result

    def _normalize_region(self, region):  # type: (Optional[str]) -> str
        """Gets the long name of the region used in the pricing API 

        This is utilized to make it more user-friendly for input data        

        return: Long name to match the pricing API index data
        """
        region = region or self.default_region
        if not region:
            raise ValueError("No region is set.")

        if region in REGION_SHORTS:  # Use long-name to match pricing API
            region = REGION_SHORTS[region]
        return region

    # type: (Optional[str]) -> str
    def _normalize_resource_type(self, type: str):
        """Gets the correct product family name used in the pricing API index data

        This is utilized to make it more user-friendly for input data

        return: the product family name used in the pricing API index data
        """
        type = type or self.default_resource_type

        if not type:
            raise ValueError("No resource type is set.")

        if type in RESOURCE_TYPES_MAPPING:  # Use product family to match pricing API
            type = RESOURCE_TYPES_MAPPING[type]
        return type
