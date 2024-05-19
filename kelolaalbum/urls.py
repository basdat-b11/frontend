from django.urls import path
from .views import *

app_name = 'daftar_album_song'

urlpatterns = [
    path('list-album/', list_album, name='list_album'),
    path('create-album/', create_album, name='create_album'),
    path('list-album-song/<str:album_id>', list_song_album, name='list_album_song'),
    path('delete-album/<str:album_id>', delete_album, name='delete_album'),
    path('delete-song/<str:song_id>', delete_song, name='delete_song'),   
]