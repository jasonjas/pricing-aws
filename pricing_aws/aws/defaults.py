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
        'operatingsystem': 'RHEL',
        'tenancy': 'Shared',
        'licensemodel': 'No License required',
        'preinstalledsw': 'NA',
        'capacitystatus': 'Used',
        'marketoption': 'OnDemand'
    }


@implements("ebs_default_attributes")
def ebs_default_attributes():  # type: () -> Dict[str,str]
    return {
        'volumeapiname': 'gp3'
    }


@implements("s3_default_attributes")
def s3_default_attributes():  # type: () -> Dict[str,str]
    return {
        'storageclass': 'General Purpose'
    }


@implements("rds_default_attributes")
def rds_default_attributes():  # type: () -> Dict[str,str]
    return {
        'instancetype': 'db.r5.4xlarge',
        'databaseengine': 'SQL Server',
        'licensemodel': 'License included',
        'deploymentoption': 'Single-AZ',
        'databaseedition': 'Standard',
    }


@implements("rds_data_default_attributes")
def rds_data_default_attributes():  # type: () -> Dict[str,str]
    return {
        'databaseengine': 'SQL Server',
        'storageMedia': 'SSD',
        'deploymentoption': 'Single-AZ',
        'usagetype': 'RDS:GP3-Storage',
        'volumetype': 'General Purpose (SSD)'
    }

@implements("ebs_snapshot_default_attributes")
def ebs_snapshot_default_attributes(): # type: () -> Dict[str,str]
   return {
        'usagetype': 'EBS:SnapshotUsage'
    }


@implements("rds_snapshot_default_attributes")
def rds_snapshot_default_attributes(): # type: () -> Dict[str,str]
   return {
        'databaseengine': 'Any',
        'databaseedition': 'Any',
        'usagetype': 'RDSCustom:ChargedBackupUsage'
    }
