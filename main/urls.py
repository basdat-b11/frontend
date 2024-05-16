from django.urls import path
from main.views import *;

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('', my_view, name='my_view'),
    path('create-album', create_album, name='create_album'), 
    path('list-album', list_album, name='list_album'),
    path('list-album-label', list_album_label, name='list_album_label'),
    path('create-lagu', create_lagu, name='create_lagu'),
    path('cek-royalti', cek_royalti, name='cek_royalti'),
    path('lagulist-album', lagulist_album, name='lagulist_album'),
    path('lagulist-album-label', lagulist_album_label, name='lagulist_album_label'),
    path('test', test_akun, name='test_akun')
]