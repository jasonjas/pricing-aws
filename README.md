# pricing-aws
Get pricing for some AWS services by processing an Excel file containing the resources you want to create.

Uses the AWS pricing API to populate local databases.

## Endpoints

* `/pricing_aws` - Site to upload Excel files and get the data once it's complete
* `/pricing_aws/purge` - Site to delete all leftover files or database entries for any that may have been left

## Django
Run the following commands to populate the django database

```
python manage.py migrate --run-syncdb
python manage.py makemigrations website
python manage.py migrate website
```

Run the following command to start Django
`pyt .\manage.py runserver`
