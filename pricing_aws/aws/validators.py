import os
from django.core.exceptions import ValidationError
from django.core.files import uploadedfile
from base64 import b64encode


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def isExcelDoc(file):
    excelSigs = [
        ('xlsx', b'\x50\x4B\x05\x06', 2, -22, 4),
        ('xls', b'\x09\x08\x10\x00\x00\x06\x05\x00', 0, 512, 8),  # Saved from Excel
        ('xls', b'\x09\x08\x10\x00\x00\x06\x05\x00',
         0, 1536, 8),  # Saved from LibreOffice Calc
        ('xls', b'\x09\x08\x10\x00\x00\x06\x05\x00',
         0, 2048, 8)  # Saved from Excel then saved from Calc
    ]

    if type(file) == uploadedfile.TemporaryUploadedFile:
        data = file.temporary_file_path()

        for sigType, sig, whence, offset, size in excelSigs:
            with open(data, 'rb') as f:
                f.seek(offset, whence)
                bytes = f.read(size)

                if bytes == sig:
                    return True
    else:
        raise ValidationError('Unable to read file on server')

    raise ValidationError('Unsupported file type!')
