from django.urls import path
from main.views import *;

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('', my_view, name='my_view'),
    path('create-album', create_album, name='create_album'), 
    path('list-album', list_album, name='list_album'),
    path('create-lagu', create_lagu, name='create_lagu'),
    path('test', test_akun, name='test_akun')
]