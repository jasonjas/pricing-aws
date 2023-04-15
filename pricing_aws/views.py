from django.http import StreamingHttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import render
from pricing_aws.aws.upload import UploadFileForm, handle_uploaded_file, PurgeDocumentsForm, PurgeStaleDocuments
import os
from website.settings import MEDIA_ROOT, BASE_DIR
from pricing_aws.aws import process_excel_file
from rest_framework.views import APIView
import os


class ProcessExcelDocument(APIView):
    """
    Return Excel document information
    """

    def post(self, request):
        message = 'Upload a single Excel file to get the AWS prices!'
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = handle_uploaded_file(docfile=request.FILES["docfile"])
                newdoc.save()
                src_path = os.path.join(MEDIA_ROOT, newdoc.docfile.path)
                process_excel_file(src_path, src_path)
                with open(src_path, 'rb') as rb:
                    response = StreamingHttpResponse(rb.readlines())
                response[
                    'Content-Disposition'] = f"attachment; filename={os.path.basename(src_path)}"
                response['Content-Length'] = os.path.getsize(src_path)
                newdoc.delete()
                return response
            else:
                message = 'The form is not valid. Fix the following error:'
        documents = handle_uploaded_file.objects.all()
        context = {'documents': documents, 'form': form, 'message': message}
        return render(request, 'list.html', context)

    def get(self, request):
        message = 'Upload a single Excel file to get the AWS prices!'
        form = UploadFileForm()

        documents = handle_uploaded_file.objects.all()
        context = {'documents': documents, 'form': form, 'message': message}
        return render(request, 'list.html', context)


class PurgeDocuments(APIView):
    """
    Purge all files on the server and the database records pointing to them
    """

    def post(self, request):
        form = PurgeDocumentsForm(request.POST)
        if form.is_valid():
            purge_status = PurgeStaleDocuments.purge_docs(password=request.POST.get("text"))
            return self.get(request, purge_status)
        
        return self.get(request, "Form was invalid")

    def get(self, request, message="Do you want to purge all of the documents?"):
        form = PurgeDocumentsForm()
        documents = handle_uploaded_file.objects.all()
        context = {'documents': documents, 'form': form, 'message': message}
        return render(request, 'purge.html', context)

class GenPassword(APIView):
    
    def get(self, file_location=f'{BASE_DIR}/pw.txt'):
        pw = get_random_string(length=12)
        with open(file_location, 'w') as flw:
            flw.write(pw)
        

    