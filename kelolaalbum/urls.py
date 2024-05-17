from django.urls import path
from .views import (list_album)

app_name = 'daftar_album_song'

urlpatterns = [
    path('list-album/', list_album, name='list-album/'),
]