from django import forms
from django.db import models
# from django.shortcuts import render
from manage_offers import create_update_databases, get_local_offers


offers = ""


# class UpdateCreateDatabases():
#     """
#     Get information about databases
#     """
#     # Need to capture the output real-time to update the database_status.html page

#     def update_dbs(self, request, offer):
#         render(request, 'database_status.html', create_update_databases(offer))


class PricingRegionSelection(forms.Form):
    region = forms.CharField(label='AWS Region', max_length=100,
                             required=False, initial="us-east-1", show_hidden_initial=True)


class HandleOffers(models.Model):
    def __init__(self, offer_name) -> None:
        offer = models.TextField(offer_name)


class GetOffers():
    """
    Put and get available offer lists in the django DB
    """

    def __init__(self) -> None:
        pass

    def get_offers(self, region=None):
        offers = get_local_offers(region)
        for offer in offers:
            HandleOffers(offer)
