from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import json
from django.http import JsonResponse

def podcast_detail(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'podcast_detail.html', context)

# def podcast_detail(request):
#     judul_podcast = "apakek"
#     genre = []
#     nama_podcaster = ""
#     total_durasi = ""
#     tanggal_rilis = ""
#     tahun = ""

#     with connection.cursor() as cursor:
#         cursor.execute("Set search_path to marmut;")
#         cursor.execute("""
#                         SELECT 
#                         """)