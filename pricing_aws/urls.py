from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProcessExcelDocument.as_view(), name='process-file'),
    path('purge', views.PurgeDocuments.as_view(), name='purge-files'),
    path('gen-pass', views.GenPassword.as_view()),
    path('update-prices', views.PopulatePrices.as_view(), name='update-prices')
]
