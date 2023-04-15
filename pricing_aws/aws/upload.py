from django import forms
from django.db import models
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from .validators import validate_file_extension, isExcelDoc
import django.core.validators

django.core.validators.BaseValidator

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()
    docfile = forms.FileField(label='Select a file', help_text='help text here', error_messages={
                              '1': "This is an error message"}, validators=[FileExtensionValidator(['xlsx','xls']), isExcelDoc])


class handle_uploaded_file(models.Model):
    docfile = models.FileField(upload_to="test", validators=[isExcelDoc])


class MyCommand(BaseCommand):
    def handle(self, *args, **options):
        content_file = ContentFile(b"Hello world!", name="hello-world.txt")
        instance = handle_uploaded_file(file_field=content_file)
        instance.save()
