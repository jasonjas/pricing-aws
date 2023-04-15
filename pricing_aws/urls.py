from django.urls import path
from . import views
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.ProcessExcelDocument.as_view(), name='process-file')
]
