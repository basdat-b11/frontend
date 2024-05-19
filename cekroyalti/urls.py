from django.urls import path
from .views import *

app_name = 'daftar_royalti'

urlpatterns = [
    path('list-royalti/', list_royalti, name='list_royalti'),
]