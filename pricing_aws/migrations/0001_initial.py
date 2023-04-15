# Generated by Django 4.2 on 2023-04-15 18:09

from django.db import migrations, models
import pricing_aws.aws.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='handle_uploaded_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='test', validators=[pricing_aws.aws.validators.isExcelDoc, pricing_aws.aws.validators.validate_file_extension])),
            ],
        ),
    ]
