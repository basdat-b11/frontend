from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
import json

# Create your views here.
def create_album(request):
    # Lakukan operasi atau logika yang diperlukan
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'create_album.html', context)

def list_album(request):
    # Lakukan operasi atau logika yang diperlukan
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'list_album.html', context)

def my_view(request):
    # Lakukan operasi atau logika yang diperlukan
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'main.html', context)

def create_lagu(request):
    # Lakukan operasi atau logika yang diperlukan
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'create_lagu.html', context)


def test_akun(request):
    result = ""
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("SELECT * FROM akun;")
        result = cursor.fetchall()
    
    print(result)
    return HttpResponse(result, content_type='application/json', status=200)