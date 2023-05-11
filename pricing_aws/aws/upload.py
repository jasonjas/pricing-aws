from django import forms
from django.db import models
from django.core.validators import FileExtensionValidator
from .validators import isExcelDoc
from django.conf import settings
import os


class UploadFileForm(forms.Form):
    """
    Form for uploading files
    """
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()
    docfile = forms.FileField(label='Select an Excel file', error_messages={
                              '1': "This is an error message"}, validators=[FileExtensionValidator(['xlsx', 'xls'])])


class handle_uploaded_file(models.Model):
    """
    Manage the files selected in the form for upload
    """
    docfile = models.FileField(
        upload_to=settings.FILES_DIRECTORY, validators=[isExcelDoc])


class PurgeDocumentsForm(forms.Form):
    text = forms.CharField(label='password', max_length=100)


class PurgeStaleDocuments():
    """
    Purge all files on the server and the database records pointing to them
    """

    def purge_docs(password_file=f'{settings.BASE_DIR}/pw.txt'):
        with open(password_file, 'r') as pwf:
            password = pwf.read()

        if settings.PURGE_PASSWORD == password:
            try:
                objects = handle_uploaded_file.objects.all()
                files_dir = os.path.join(
                    settings.MEDIA_ROOT, settings.FILES_DIRECTORY)

                files = os.listdir(files_dir)
                print(objects)
                a = objects.delete()
                for file in files:
                    if file != ".keep":
                        os.remove(os.path.join(files_dir, file))
            except:
                raise ValueError(
                    "Error removing documents and clearing database entries.")

        else:
            return "Password was incorrect."
        return "Successfully removed files and entries from the database."
