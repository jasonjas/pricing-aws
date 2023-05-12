# AWS Pricing
Get pricing for AWS resources from resources defined in an Excel spreadsheet

## Column headings
These are the headings that can be used for getting prices.

## Global headings (required)
### <ins>type</ins>
Possible values: (description)
  * ec2: Compute Instance
  * rds: Database Instance
  * rds-data: Database Storage
  * ebs: Storage
  * snapshot: Storage Snapshot
  * s3: Storage
  * vpc: AmazonVPC
  * lambda: Serverless

### <ins>region</ins>
The region name, Example values:
* us-east-1
* eu-central-1

## EC2 instance
Heading: (Description)
* type = ec2
* instanceType: Size of instance (ex. m5.large)
* region: region name
* capacitystatus: See capacitystatus in Definitions below
* marketoption: (ex. OnDemand, etc)
* preInstalledSw: Refers to pre-installed software like SQL, for a default 'normal' instance use 'NA'

## EBS disk
Heading: (Description)
* type = ebs
* volumeapiname: disk type (ex. gp2, gp3, io1, etc)
* storage-size-gb: size in GB of the EBS volume

## Snapshots
Heading: (Description)
* type = snapshot
* storage-size-gb: size in GB of the EBS volume

## RDS instance
Heading: (Description)
* type = rds
* instanceType: Size of instance (ex. db.m5.large)
* databaseengine: engine name (ex. Oracle, MySQL, SQL Server, PostreSQL)
* licensemodel: license model (License included, License not required, etc)
* deploymentoption: Single-AZ or Multiple-AZ
* databaseedition: edition of DB, not all have one (ex. Standard Two, Stardard, etc)

## RDS data
* type = rds_data
* storageMedia: type of storage media (ex. SSD)
* databaseengine: engine name (ex. Oracle, MySQL, SQL Server, PostreSQL)
* usagetype: Type of usage (ex. RDS:GP3-Storage, RDS:GP2-Storage, etc)
* deploymentoption: Single-AZ or Multiple-AZ
* volumetype: type of volume (ex. 'General Purpose (SSD)')
* storage-size-gb: size in GB of the EBS volume

## S3 storage
Heading: (Description)
* type = s3
* storageclass: class of storage (ex. General Purpose, etc)
* storage-size-gb: size in GB of the EBS volume

## Lambda function
Heading: (Description)
* type = lambda


# Definitions
## capacitystatus
The on-demand/reservation type. Examples include:
* Used
* AllocatedCapacityReservation
* UnusedCapacityReservation