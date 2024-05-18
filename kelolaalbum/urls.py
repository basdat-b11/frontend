from django.urls import path
from .views import *

app_name = 'daftar_album_song'

urlpatterns = [
    path('list-album/', list_album, name='list_album'),
    path('create-album/', create_album, name='create-album/'),
]