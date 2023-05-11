from time import sleep
from django.http import StreamingHttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import render
from pricing_aws.aws.upload import UploadFileForm, handle_uploaded_file, PurgeDocumentsForm, PurgeStaleDocuments
from pricing_aws.aws.databases import PricingRegionSelection, HandleOffers, GetOffers
import os
from website.settings import MEDIA_ROOT, BASE_DIR
from pricing_aws.aws import process_excel_file
from rest_framework.views import APIView
import os


class ProcessExcelDocument(APIView):
    """
    Return Excel document information
    """

    def post(self, request, offers = ""):
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
            purge_status = PurgeStaleDocuments.purge_docs(
                password=request.POST.get("text"))
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


class PopulatePrices(APIView):
    def post(self, request, first_run=True):
        """
        Update/create the databases
        """
        form = PricingRegionSelection(request.POST)
        if form.is_valid():
            # GET OFFER NAMES FROM DATABASE
            offer_list = HandleOffers.objects.all()
            print(offer_list)
            # VERIFY DB RESULTS ARE NOT EMPTY OR NULL
            if not offer_list and not first_run:
                status = "Databases were successfully updated"
                return self.get(request, message=None, status=status)
            if first_run:
                message = "Getting offer data"
                status = "Please wait for offer files to download"
                status = self.update_status(request, message, status)
                new_offers = GetOffers.get_offers(request.POST.get("region"))
            else:
                # GET NEXT OFFER IN LIST
                offer = offer_list[0]
                # UPDATE STATUS MESSAGE
                message = f"Updating databases for offer {offer}"
                status = self.update_status(request, message)
                # UPDATE OFFER IN DATABASE
                handled_offer = HandleOffers(offer)
                handled_offer.delete()
                # RETURN POST WITH MESSAGE
            return self.post(request, first_run=False)
        

    def get(self, request, message=None, status='Status...'):
        """
        Site to initialize the updates
        """
        if message == None:
            message = "Update databases containing pricing data.\n \
                Enter a region if you want pricing data to be for a specific region; otherwise leave it blank for all regions."
        form = PricingRegionSelection()
        context = {'message': message, 'form': form, 'status': status}
        return render(request, 'database.html', context)
    

    def update_status(self, request, message, status):
        # return self.get(request, message, status)
        context = {'message': message, 'status': status}
        return render(request, 'database_status.html', context)
