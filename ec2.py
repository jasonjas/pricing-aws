from collections import defaultdict
import logging

from typing import Any, Dict, List, Optional, Set, Type  # noqa

import six

from .constants import (
    REGION_SHORTS,
    EC2_LEASE_CONTRACT_LENGTH,
    EC2_OFFERING_CLASS,
    EC2_PURCHASE_OPTION,
    RDS_LEASE_CONTRACT_LENGTH,
    RDS_OFFERING_CLASS,
    RDS_PURCHASE_OPTION,
    HOURS_IN_YEAR
)



OFFER_CLASS_MAP = {}

class EC2Offer:

    def __init__(self, *args, **kwargs):
        super(EC2Offer, self).__init__(*args, **kwargs)

        self.default_operating_system = 'RHEL'
        self.default_tenancy = 'Shared'
        self.default_license_model = 'No License required'
        self.default_preinstalled_software = 'NA'
        self.default_capacitystatus = 'Used'
        self.product_family = 'Compute Instance'

    def required_attributes(self):
        self.default_tenancy


        self._reverse_sku = self._generate_reverse_sku_mapping(
            'instanceType', 'usagetype', 'tenancy', 'licenseModel',
            'preInstalledSw', 'location', 'capacitystatus',
            # Both families are queried assuming that instance names will never clash between
            # them. This should be true given metal instance naming conventions thus far (instance
            # size is 'metal').
            product_families=['Compute Instance', 'Compute Instance (bare metal)']
        )

        # Lazily-loaded cache to hold offerTermCodes within a SKU
        self._reserved_terms_to_offer_term_code = defaultdict(dict)

    def get_sku(self,
                instance_type,               # type: str
                operating_system=None,       # type: Optional[str]
                tenancy=None,                # type: Optional[str]
                license_model=None,          # type: Optional[str]
                preinstalled_software=None,  # type: Optional[str]
                region=None,                 # type: Optional[str]
                capacitystatus=None         # type: Optional[str]
                ):
        # type: (...) -> str
        region = self._normalize_region(region)
        operating_system = operating_system or self.default_operating_system
        tenancy = tenancy or self.default_tenancy
        license_model = license_model or self.default_license_model
        preinstalled_software = (preinstalled_software or
                                 self.default_preinstalled_software)
        capacitystatus = capacitystatus or self.default_capacitystatus

        attributes = [instance_type, operating_system, tenancy, license_model,
                      preinstalled_software, region, capacitystatus]
        if not all(attributes):
            raise ValueError("All attributes are required: {}"
                             .format(attributes))
        sku = self._reverse_sku.get(self.hash_attributes(*attributes))
        if sku is None:
            raise ValueError("Unable to lookup SKU for attributes: {}"
                             .format(attributes))
        return sku

    def ondemand_hourly(self,
                        instance_type,               # type: str
                        operating_system=None,       # type: Optional[str]
                        tenancy=None,                # type: Optional[str]
                        license_model=None,          # type: Optional[str]
                        preinstalled_software=None,  # type: Optional[str]
                        region=None,                 # type: Optional[str]
                        capacitystatus=None         # type: Optional[str]
                        ):
        # type: (...) -> float
        sku = self.get_sku(
            instance_type,
            operating_system=operating_system,
            tenancy=tenancy,
            license_model=license_model,
            preinstalled_software=preinstalled_software,
            region=region,
            capacitystatus=capacitystatus
        )
        term = self._offer_data['terms']['OnDemand'][sku]
        price_dimensions = next(six.itervalues(term))['priceDimensions']
        price_dimension = next(six.itervalues(price_dimensions))
        raw_price = price_dimension['pricePerUnit']['USD']
        return float(raw_price)

    def reserved_hourly(self,
                        instance_type,                               # type: str
                        operating_system=None,                       # type: Optional[str]
                        tenancy=None,                                # type: Optional[str]
                        license_model=None,                          # type: Optional[str]
                        preinstalled_software=None,                  # type: Optional[str]
                        lease_contract_length=None,                  # type: Optional[str]
                        offering_class=EC2_OFFERING_CLASS.STANDARD,  # type: str
                        purchase_option=None,                        # type: Optional[str]
                        amortize_upfront=True,                       # type: bool
                        region=None,                                 # type: Optional[str]
                        capacitystatus=None,                        # type: Optional[str]
                        ):
        # type: (...) -> float
        self._validate_reserved_price_args(
            lease_contract_length, offering_class, purchase_option)

        assert lease_contract_length is not None
        assert offering_class is not None
        assert purchase_option is not None

        sku = self.get_sku(
            instance_type,
            operating_system=operating_system,
            tenancy=tenancy,
            license_model=license_model,
            preinstalled_software=preinstalled_software,
            region=region,
            capacitystatus=capacitystatus
        )

        term_attributes = [
            lease_contract_length,
            offering_class,
            purchase_option
        ]
        term = self._get_reserved_offer_term(sku, term_attributes)

        price_dimensions = term['priceDimensions'].values()
        hourly_dimension = next(d for d in price_dimensions
                                if d['unit'].lower() == 'hrs')
        upfront_dimension = next((d for d in price_dimensions
                                  if d['description'] == 'Upfront Fee'), None)

        raw_hourly = hourly_dimension['pricePerUnit']['USD']
        raw_upfront = upfront_dimension['pricePerUnit']['USD'] if upfront_dimension else 0

        hourly = float(raw_hourly)
        upfront = float(raw_upfront)

        if amortize_upfront:
            hours = self._get_hours_in_lease_contract_length(
                lease_contract_length)
            hourly += (upfront / hours)

        return hourly

    def _get_reserved_offer_term(self, sku, term_attributes):
        # type: (str, List[str]) -> Dict[str, Any]
        term_attributes_hash = self.hash_attributes(*term_attributes)
        all_terms = self._offer_data['terms']['Reserved'][sku]
        sku_terms = self._reserved_terms_to_offer_term_code[sku]
        if term_attributes_hash not in sku_terms:
            for term_sku, term in six.iteritems(all_terms):
                hashed = self._hash_reserved_term_attributes(term)
                sku_terms[hashed] = term['offerTermCode']

        code = sku_terms[term_attributes_hash]
        return all_terms['.'.join([sku, code])]

    def _hash_reserved_term_attributes(self, term):
        attrs = term['termAttributes']
        return self.hash_attributes(
            attrs['LeaseContractLength'],
            attrs['OfferingClass'],
            attrs['PurchaseOption']
        )

    @classmethod
    def _get_hours_in_lease_contract_length(cls, lease_contract_length):
        if lease_contract_length == '1yr':
            return cls.HOURS_IN_YEAR
        elif lease_contract_length == '3yr':
            return 3 * cls.HOURS_IN_YEAR
        raise ValueError("Unknown lease contract length: {}"
                         .format(lease_contract_length))

    def reserved_upfront(self,
                         instance_type,                               # type: str
                         operating_system=None,                       # type: Optional[str]
                         tenancy=None,                                # type: Optional[str]
                         license_model=None,                          # type: Optional[str]
                         preinstalled_software=None,                  # type: Optional[str]
                         lease_contract_length=None,                  # type: Optional[str]
                         offering_class=EC2_OFFERING_CLASS.STANDARD,  # type: str
                         purchase_option=None,                        # type: Optional[str]
                         region=None,                                 # type: Optional[str]
                         capacitystatus=None,                        # type: Optional[str]
                         ):
        # type: (...) -> float
        self._validate_reserved_price_args(
            lease_contract_length, offering_class, purchase_option)

        assert lease_contract_length is not None
        assert offering_class is not None
        assert purchase_option is not None

        sku = self.get_sku(
            instance_type,
            operating_system=operating_system,
            tenancy=tenancy,
            license_model=license_model,
            preinstalled_software=preinstalled_software,
            region=region,
            capacitystatus=capacitystatus
        )

        term_attributes = [
            lease_contract_length,
            offering_class,
            purchase_option
        ]
        term = self._get_reserved_offer_term(sku, term_attributes)

        price_dimensions = term['priceDimensions'].values()
        upfront_dimension = next((d for d in price_dimensions
                                  if d['description'] == 'Upfront Fee'), None)

        raw_upfront = upfront_dimension['pricePerUnit']['USD'] if upfront_dimension else 0
        return float(raw_upfront)

    @classmethod
    def _validate_reserved_price_args(cls,
                                      lease_contract_length,  # type: Optional[str]
                                      offering_class,         # type: Optional[str]
                                      purchase_option,        # type: Optional[str]
                                      ):
        # type: (...) -> None
        if lease_contract_length not in EC2_LEASE_CONTRACT_LENGTH.values():
            valid_options = EC2_LEASE_CONTRACT_LENGTH.values()
            raise ValueError(
                "Lease contract '{}' is invalid. Valid options are: {}"
                .format(lease_contract_length, valid_options)
            )

        if offering_class not in EC2_OFFERING_CLASS.values():
            valid_options = EC2_OFFERING_CLASS.values()
            raise ValueError(
                "Offering class '{}' is invalid. Valid options are: {}"
                .format(offering_class, valid_options)
            )

        if purchase_option not in EC2_PURCHASE_OPTION.values():
            valid_options = EC2_PURCHASE_OPTION.values()
            raise ValueError(
                "Purchase option '{}' is invalid. Valid options are: {}"
                .format(purchase_option, valid_options)
            )

        if (lease_contract_length == EC2_LEASE_CONTRACT_LENGTH.ONE_YEAR and
                offering_class == 'convertible'):
            raise ValueError("The convertible offering class is not available "
                             "on a 1year lease.")
