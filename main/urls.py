from django.urls import path
from main.views import test_akun, playlist, song_detail, kelola_playlist

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('', test_akun, name='test_akun'), 
    path('kelola_playlist/', kelola_playlist, name='kelola_playlist'),
    path('song_detail/', song_detail, name='song_detail'),
    path('playlist/', playlist, name='playlist'),
]