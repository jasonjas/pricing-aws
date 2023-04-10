from typing import Dict  # noqa


class Enum(object):
    """Very simple string enumeration implementation.

    Basic usage: `Colors = Enum('red', 'blue', 'green')  # Colors.RED == 'red'`

    You may also use kwargs to override accessor names.
    ```
    Years = Enum(one_year='1yr')  # Years.ONE_YEAR == '1yr'
    ```
    """

    def __init__(self, *args, **kwargs):  # type: (*str, **str) -> None
        self._values = {}  # type: Dict[str, str]
        for arg in args:
            self._values[arg.upper()] = arg
        for kwarg in kwargs:
            value = kwargs[kwarg]
            self._values[kwarg.upper()] = value

    def __getattr__(self, attr):
        if attr not in self._values:
            raise AttributeError("Enum value '{}' doesn't exist.".format(attr))
        return self._values[attr]

    def values(self):
        return self._values.values()


OFFER_BASE_URL = 'https://pricing.us-east-1.amazonaws.com'
OFFER_INDEX_ENDPOINT = '/offers/v1.0/aws/index.json'

AVAILABLE_OFFERS_MAP = {
    'AmazonS3': 's3',
    'AmazonEC2': 'ec2',
    'AmazonRDS': 'rds',
    'AWSLambda': 'lambda',
    'AmazonVPC': 'vpc'
}

# these values match up with the 'productfamily' value
RESOURCE_TYPES_MAPPING = {
    'ec2': 'Compute Instance',
    'rds': 'Database Instance',
    'rds-data': 'Database Storage',
    'ebs': 'Storage',
    'snapshot': 'Storage Snapshot',
    's3': 'Storage',
    'vpc': 'AmazonVPC',
    'lambda': 'Serverless'
}

DB_NAME_MAPPING = {
    'ec2': 'ec2',
    'rds': 'rds',
    'rds-data': 'rds',
    'ebs': 'ec2',
    'snapshot': 'ec2',
    's3': 's3',
    'vpc': 'vpc',
    'lambda': 'lambda'
}

# noqa - Taken from: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html
REGION_SHORTS = {
    'us-east-1': 'US East (N. Virginia)',
    'us-east-2': 'US East (Ohio)',
    'us-west-1': 'US West (N. California)',
    'us-west-2': 'US West (Oregon)',
    'ca-central-1': 'Canada (Central)',
    'eu-north-1': 'EU (Stockholm)',
    'eu-west-1': 'EU (Ireland)',
    'eu-central-1': 'EU (Frankfurt)',
    'eu-west-2': 'EU (London)',
    'eu-west-3': 'EU (Paris)',
    'ap-northeast-1': 'Asia Pacific (Tokyo)',
    'ap-northeast-2': 'Asia Pacific (Seoul)',
    'ap-northeast-3': 'Asia Pacific (Osaka-Local)',
    'ap-southeast-1': 'Asia Pacific (Singapore)',
    'ap-southeast-2': 'Asia Pacific (Sydney)',
    'ap-south-1': 'Asia Pacific (Mumbai)',
    'sa-east-1': 'South America (Sao Paulo)',  # intentionally no unicode,
    'us-gov-west-1': 'AWS GovCloud (US)',
    'us-gov-east-1': 'AWS GovCloud (US-East)'
}

EC2_LEASE_CONTRACT_LENGTH = Enum(one_year='1yr', three_year='3yr')
EC2_OFFERING_CLASS = Enum('standard', 'convertible')
EC2_PURCHASE_OPTION = Enum(
    no_upfront='No Upfront',
    partial_upfront='Partial Upfront',
    all_upfront='All Upfront'
)

RDS_LEASE_CONTRACT_LENGTH = Enum(one_year='1yr', three_year='3yr')
RDS_OFFERING_CLASS = Enum('standard')
RDS_PURCHASE_OPTION = Enum(
    no_upfront='No Upfront',
    partial_upfront='Partial Upfront',
    all_upfront='All Upfront'
)

EBS_PRODUCT_FAMILY = Enum(
    iops='System Operation',
    data='Storage'
)
EBS_STORAGE_MEDIA = Enum(
    hdd='HDD-backed',
    ssd='SSD-backed'
)
EBS_VOLUME_API_NAME = [
    'io1',
    'io2',
    'gp2',
    'gp3',
    'standard',
    'sc1'
]

SNAPSHOT_STORAGE_MEDIA = 'Amazon S3'
SNAPSHOT_PRODUCT_FAMILY = 'Storage Snapshot'
SNAPSHOT_USAGE_TYPE = Enum(
    archive_early_delete='EBS:SnapshotArchiveEarlyDelete',
    snapshot_usage='EBS:SnapshotUsage',
    archive_retrieval='EBS:SnapshotArchiveRetrieval',
    usage_under_billing='EBS:SnapshotUsageUnderBilling'
)

PRODUCTS_DATABASE_FILE_NAME = 'products.db'
TERMS_DATABASE_FILE_NAME = 'terms.db'

HOURS_IN_YEAR = 24 * 365
HOURS_IN_MONTH = HOURS_IN_YEAR / 12
