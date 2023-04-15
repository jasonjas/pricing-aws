from django.http import HttpResponseRedirect
from django.shortcuts import render
from pricing_aws.aws.upload import UploadFileForm, handle_uploaded_file
import os
from website.settings import MEDIA_ROOT
from pricing_aws.aws import process_excel_file
from rest_framework.views import APIView
import os
from django.core.exceptions import ValidationError


class ProcessExcelDocument(APIView):
    """
    Return Excel document information
    """

    def post(self, request):
        message = 'Upload as many files as you want!'
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = handle_uploaded_file(docfile=request.FILES["docfile"])
                try:
                    newdoc.full_clean()
                except ValidationError:
                    message = 'Invalide file data type!'
                newdoc.save()
                src_path = os.path.join(MEDIA_ROOT, newdoc.docfile.path)
                process_excel_file(src_path, src_path)
                # return HttpResponseRedirect('')
            else:
                message = 'The form is not valid. Fix the following error:'
        documents = handle_uploaded_file.objects.all()
        context = {'documents': documents, 'form': form, 'message': message}
        return render(request, 'list.html', context)
        

    def get(self, request):
        message = 'Upload as many files as you want!'
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = handle_uploaded_file(docfile=request.FILES["docfile"])
                newdoc.save()
                return HttpResponseRedirect("process-file")
            else:
                message = 'The form is not valid. Fix the following error:'
        else:
            form = UploadFileForm()

        documents = handle_uploaded_file.objects.all()
        context = {'documents': documents, 'form': form, 'message': message}
        return render(request, 'list.html', context)


class UploadPage(APIView):
    """
    Return site to upload file
    """

    def get(self, request):
        return render(request, 'upload.html')
