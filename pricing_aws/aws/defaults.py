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
def ec2_default_attributes():  # type: () -> Dict[str,str]
    return {
        'attributes_operatingsystem': 'RHEL',
        'attributes_tenancy': 'Shared',
        'attributes_licensemodel': 'No License required',
        'attributes_preinstalledsw': 'NA',
        'attributes_capacitystatus': 'Used',
        'attributes_marketoption': 'OnDemand'
    }


@implements("ebs_default_attributes")
def ebs_default_attributes():  # type: () -> Dict[str,str]
    return {
        'attributes_volumeapiname': 'gp3'
    }


@implements("s3_default_attributes")
def s3_default_attributes():  # type: () -> Dict[str,str]
    return {
        'attributes_storageclass': 'General Purpose'
    }


@implements("rds_default_attributes")
def rds_default_attributes():  # type: () -> Dict[str,str]
    return {
        'attributes_instancetype': 'db.r5.4xlarge',
        'attributes_databaseengine': 'SQL Server',
        'attributes_licensemodel': 'License included',
        'attributes_deploymentoption': 'Single-AZ',
        'attributes_databaseedition': 'Standard',
    }


@implements("rds_data_default_attributes")
def rds_data_default_attributes():  # type: () -> Dict[str,str]
    return {
        'attributes_databaseengine': 'SQL Server',
        'attributes_storageMedia': 'SSD',
        'attributes_deploymentoption': 'Single-AZ',
        'attributes_usagetype': 'RDS:GP3-Storage',
        'attributes_volumetype': 'General Purpose (SSD)'
    }

@implements("ebs_snapshot_default_attributes")
def ebs_snapshot_default_attributes(): # type: () -> Dict[str,str]
   return {
        'attributes_usagetype': 'EBS:SnapshotUsage'
    }


@implements("rds_snapshot_default_attributes")
def rds_snapshot_default_attributes(): # type: () -> Dict[str,str]
   return {
        'attributes_databaseengine': 'any',
        'attributes_databaseedition': 'any',
        'attributes_usagetype': 'RDSCustom:ChargedBackupUsage'
    }
