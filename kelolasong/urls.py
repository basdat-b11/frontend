from django.urls import path
from . import views

app_name = 'kelolasong'

urlpatterns = [
    path('createsong/<str:album_id>', views.create_song_artist, name='create_song'),
]