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
* capacitystatus: See 
* marketoption
* preInstalledSw

## EBS disk
* type = ebs

## Snapshots
* type = snapshot

## RDS instance
* type = rds

## S3 storage
* type = s3

## Lambda function
* type = lambda


# Definitions
## capacitystatus
The on-demand/reservation type. Examples include:
* Used
* AllocatedCapacityReservation
* UnusedCapacityReservation