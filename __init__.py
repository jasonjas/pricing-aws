import requests
from requests.adapters import HTTPAdapter
from typing import Dict, Type  # noqa
from pathlib import PurePosixPath

from offers import AWSOffer, get_offer_class  # noqa
from cache import maybe_read_from_cache, maybe_write_to_cache
from get_offers import _get_offers, _fetch_offer


__version__ = "0.1.0"

_SERVICES = {}  # type: Dict[str, Type[AWSOffer]]


def all_service_names():
    return _get_offers().keys()


def offer(service_name, region=None, version='current'):
    if service_name not in _SERVICES:
        offer_data = _fetch_offer(service_name, region=region, version=version)
        _SERVICES[service_name] = get_offer_class(service_name)(offer_data)
    return _SERVICES[service_name]
