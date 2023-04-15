import os
from django.core.exceptions import ValidationError
from django.core.files import uploadedfile
from base64 import b64encode


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def is_xslx(filename):
    with open(filename, 'rb') as f:
        first_four_bytes = f.read(4)


def isExcelDoc(file):
    excelSigs = [
        ('xlsx', b'\x50\x4B\x05\x06', 2, -22, 4),
        ('xls', b'\x09\x08\x10\x00\x00\x06\x05\x00', 0, 512, 8),  # Saved from Excel
        ('xls', b'\x09\x08\x10\x00\x00\x06\x05\x00',
         0, 1536, 8),  # Saved from LibreOffice Calc
        ('xls', b'\x09\x08\x10\x00\x00\x06\x05\x00',
         0, 2048, 8)  # Saved from Excel then saved from Calc
    ]

    if type(file) == uploadedfile.InMemoryUploadedFile:
        for sigType, sig, whence, offset, size in excelSigs:
            file.open().seek(offset, whence)
            bytes = file.read(size)
            if bytes == sig:
                return True

    if type(file) == uploadedfile.TemporaryUploadedFile:
        data = file.temporary_file_path()
        # with open(os.path.join('c:\\', 'temp', 'test.txt'), 'w') as w:
        #     w.writelines(file.chunks())
        # uploadedfile.InMemoryUploadedFile.open(mode=)

        for sigType, sig, whence, offset, size in excelSigs:
            with open(data, 'rb') as f:
                f.seek(offset, whence)
                bytes = f.read(size)

                if bytes == sig:
                    return True

    raise ValidationError('Unsupported file type.')
