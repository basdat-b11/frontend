from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import json
from django.http import JsonResponse

def create_podcast(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'create_podcast.html', context)


email_pembuat = 'mark48@gmail.com'
def list_podcast(request):


    with connection.cursor() as cursor:
        cursor.execute("SET search_path to marmut;")
        cursor.execute("""
                        SELECT 
                            K.judul AS Judul_Podcast,
                            K.tanggal_rilis AS Tanggal_Rilis,
                            K.durasi AS Durasi,
                            P.email_podcaster AS Email_Podcaster,
                            COUNT(E.id_episode) AS Jumlah_Episode,
                            P.id_konten
                        FROM 
                            PODCAST P
                        JOIN 
                            KONTEN K ON P.id_konten = K.id
                        JOIN 
                            PODCASTER PC ON P.email_podcaster = PC.email
                        LEFT JOIN 
                            EPISODE E ON P.id_konten = E.id_konten_podcast
                        WHERE 
                            P.email_podcaster = %s
                        GROUP BY 
                            K.judul, K.tanggal_rilis, K.durasi, P.email_podcaster;

                        """, [email_pembuat])
        
        result = cursor.fetchall()
        podcasts = []
        for row in result:
            durasi = row[2]
            durasi_jam = durasi // 60
            durasi_menit = durasi % 60
            if durasi_jam == 0:
                durasi = str(durasi_menit) + " menit"
            else:
                durasi = str(durasi_jam) + " jam " + str(durasi_menit) + " menit"
            podcasts.append({
                'email_podcaster': row[3],
                'judul_podcast': row[0],
                'tanggal_rilis': row[1],
                'total_durasi': durasi,
                'total_episode': row[4],
                'id_konten': row[5]
            })

    context = {
        'podcasts': podcasts
    }
    return render(request, 'list_podcast.html', context)

def create_episode(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'create_episode.html', context)

def list_episode(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'list_episode.html', context)