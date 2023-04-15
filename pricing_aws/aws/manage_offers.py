from pathlib import PurePosixPath
import requests
from requests.adapters import HTTPAdapter
from constants import OFFER_BASE_URL, OFFER_INDEX_ENDPOINT, AVAILABLE_OFFERS_MAP
import json
import os
from cache import maybe_read_from_cache, maybe_write_to_cache, cache_path
from query_db import populate_products_database, populate_terms_db

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=5))
offer_dir = cache_path()


def _fetch_offers():
    cache_key = 'offers'
    offers = maybe_read_from_cache(cache_key)
    if offers is not None:
        return offers
    resp = session.get(OFFER_BASE_URL + OFFER_INDEX_ENDPOINT)
    resp.raise_for_status()
    offers = resp.json()['offers']

    maybe_write_to_cache(cache_key, offers)
    return offers


def _fetch_available_versions(offers, offer_name):
    cache_key = 'offers_version_{}'.format(offer_name)
    offers_version = maybe_read_from_cache(cache_key)
    if offers_version is not None:
        return offers_version
    offers_version_endpoint = offers[offer_name]['versionIndexUrl']
    resp = session.get(OFFER_BASE_URL + offers_version_endpoint)
    resp.raise_for_status()
    offers_version = resp.json()['versions']

    maybe_write_to_cache(cache_key, offers_version)
    return offers_version


def _fetch_offer(offer_name, region=None, version='current'):
    # type: (str, str, str) -> None
    if offer_name not in AVAILABLE_OFFERS_MAP:
        raise ValueError('Unknown offer name: {}'.format(offer_name))

    offers = _fetch_offers()
    service_short_name = AVAILABLE_OFFERS_MAP[offer_name]

    region_text = ''
    if region is not None:
        region_text = f'_{region}'
    cache_key = '{}_offer_{}{}.json'.format(service_short_name, version, region_text)
    offer = maybe_read_from_cache(cache_key, False)
    if offer == 'exists':
        return
    if version == 'current':
        offer_endpoint = offers[offer_name]['currentVersionUrl']
    else:
        other_versions = _fetch_available_versions(offers, offer_name)
        if version in other_versions:
            offer_endpoint = other_versions[version]['offerVersionUrl']
        else:
            raise ValueError('Invalid version specified {}. Must be one of: [{}]'.format(
                version, ', '.join(sorted(other_versions.keys(), reverse=True))))

    if region is not None:
        posix_path = PurePosixPath(offer_endpoint)
        path_list = list(posix_path.parts)
        path_list.insert(-1, region)
        offer_endpoint = str(PurePosixPath('').joinpath(*path_list))

    resp = session.get(OFFER_BASE_URL + offer_endpoint, stream=True)
    resp.raise_for_status()
    out_file = os.path.join(offer_dir, cache_key)

    with open(out_file, 'wb') as f:
        for chunk in resp.iter_content(16*1024):
            f.write(chunk)


def create_update_databases():
    for offer in AVAILABLE_OFFERS_MAP:
        print(f'Retrieving offer {offer}')
        _fetch_offer(offer)

    offer_files = os.listdir(offer_dir)
    for of in offer_files:
        if not of.endswith('.json'):
            continue
        service = of.split('_')[0]
        file_path = os.path.join(offer_dir, of)
        print(f'populating products for {of}')
        populate_products_database(service, src_file_path=file_path, dest_file_path='products.db')
        print(f'populating terms for {of}')
        populate_terms_db(service, src_file_path=file_path, dest_file_path='terms.db')