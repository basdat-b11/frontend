from django.db import connection
from django.shortcuts import render

def kelola_playlist(request):
    return render(request, 'kelola_playlist.html')