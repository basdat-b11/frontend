from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
import uuid

from django.urls import reverse

email_pembuat = 'mark48@gmail.com'
def create_podcast(request):
    if request.method == 'POST':
        title = request.POST.get('judul')
        genres = request.POST.getlist('genres')
        id_konten = str(uuid.uuid4())

        query = """
                SET search_path to marmut;
                INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) 
                VALUES (%s, %s, CURRENT_TIMESTAMP, EXTRACT(YEAR FROM CURRENT_TIMESTAMP), 0);
                """
        
        query2 = """
                 SET search_path to marmut;
                 INSERT INTO PODCAST (id_konten, email_podcaster) 
                 VALUES (%s, %s);
                 """
        
        genre_query = """
                      SET search_path to marmut;
                      INSERT INTO GENRE (id_konten, genre) 
                      VALUES (%s, %s);
                      """

        with connection.cursor() as cursor:
            cursor.execute(query, [id_konten, title])
            cursor.execute(query2, [id_konten, email_pembuat])
            for genre in genres:
                cursor.execute(genre_query, [id_konten, genre])

        return redirect('/kelolapodcast')

    fetch_genres_query = """
        SET search_path to marmut;
        SELECT DISTINCT genre FROM GENRE;
        """

    with connection.cursor() as cursor:
        cursor.execute(fetch_genres_query)
        genres = [row[0] for row in cursor.fetchall()]

    context = {
        'genres': genres
    }

    return render(request, 'create_podcast.html', context)

def delete_podcast(request, id_podcast):
    query = """
            SET search_path to marmut;
            DELETE FROM PODCAST 
            WHERE id_konten = %s;
            """
    
    with connection.cursor() as cursor:
            cursor.execute(query, [id_podcast])

    return redirect('/kelolapodcast')

def list_podcast(request):
    query = """
            SET search_path to marmut;
            SELECT p.id_konten AS podcast_id, k.judul AS podcast_title, 
                   e.id_episode, e.judul AS episode_title, e.deskripsi, e.durasi AS episode_duration, e.tanggal_rilis AS episode_release_date,
                   g.genre, a.nama AS podcaster_name
            FROM PODCAST p
            JOIN KONTEN k ON p.id_konten = k.id
            LEFT JOIN EPISODE e ON p.id_konten = e.id_konten_podcast
            LEFT JOIN GENRE g ON k.id = g.id_konten
            LEFT JOIN PODCASTER po ON p.email_podcaster = po.email
            LEFT JOIN AKUN a ON po.email = a.email
            WHERE p.email_podcaster = %s
            ORDER BY k.judul, e.tanggal_rilis;
            """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [email_pembuat])
        rows = cursor.fetchall()

    podcasts_dict = {}
    for row in rows:
        podcast_id, podcast_title, episode_id, episode_title, episode_desc, episode_duration, episode_release_date, genre, podcaster_name = row
        
        if podcast_id not in podcasts_dict:
            podcasts_dict[podcast_id] = {
                "podcast_id": podcast_id,
                "judul_podcast": podcast_title,
                "genres": set(),
                "nama_podcaster": podcaster_name,
                "total_durasi": 0,
                "episodes": [],
                "total_episodes": 0
            }

        if episode_id:
            episode_duration = episode_duration or 0
            podcasts_dict[podcast_id]["total_durasi"] += episode_duration
            podcasts_dict[podcast_id]["episodes"].append({
                "judul_episode": episode_title,
                "deskripsi_episode": episode_desc,
                "durasi_episode": format_durasi(episode_duration),
                "tanggal_rilis_episode": episode_release_date,
            })
            podcasts_dict[podcast_id]["total_episodes"] += 1

        if genre:
            podcasts_dict[podcast_id]["genres"].add(genre)

    for podcast in podcasts_dict.values():
        podcast["total_durasi"] = format_durasi(podcast["total_durasi"])
        podcast["genres"] = ", ".join(podcast["genres"])

    content = {"podcasts": list(podcasts_dict.values())}

    return render(request, 'list_podcast.html', content)
    
def format_durasi(minutes):
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours} hour {mins} minutes"
    elif hours > 0:
        return f"{hours} hour"
    else:
        return f"{mins} minutes"

def create_episode(request, podcast_id):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        durasi = int(request.POST.get('durasi'))
        id_episode = str(uuid.uuid4())

        query = """
                SET search_path to marmut;
                INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
                """
        
        query2 =    """
                    SET SEARCH_PATH TO MARMUT;
                    UPDATE KONTEN
                    SET durasi = COALESCE(durasi, 0) + %s
                    WHERE id = %s;
                    """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_episode, podcast_id, judul, deskripsi, durasi])
            cursor.execute(query2, [durasi, podcast_id])

        return redirect('/kelolapodcast') 

    context = {
        'podcast_id': podcast_id
    }

    return render(request, 'create_episode.html', context)

def delete_episode(request, id_episode):
    query = """
            SET search_path to marmut;
            DELETE FROM EPISODE 
            WHERE id_episode = %s;
            """
    
    podcast_id_query = """
                       SET search_path to marmut;
                       SELECT id_konten_podcast FROM EPISODE
                       WHERE id_episode = %s;
                       """
    
    with connection.cursor() as cursor:
            cursor.execute(podcast_id_query, [id_episode])
            podcast_id = cursor.fetchone()[0]
            
            cursor.execute(query, [id_episode])

    return redirect(reverse('kelolapodcast:list_episode', args=[podcast_id]))

def list_episode(request, podcast_id):
    query = """
            SET search_path to marmut;
            SELECT k.judul AS podcast_title, 
                   e.id_episode, e.judul AS episode_title, e.deskripsi AS episode_desc, e.durasi AS episode_duration, e.tanggal_rilis AS episode_release_date
            FROM EPISODE e
            JOIN PODCAST p ON e.id_konten_podcast = p.id_konten
            JOIN KONTEN k ON p.id_konten = k.id
            WHERE e.id_konten_podcast = %s
            ORDER BY e.tanggal_rilis;
            """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [podcast_id])
        rows = cursor.fetchall()

    episodes = []
    podcast_title = ""
    for row in rows:
        podcast_title, episode_id, episode_title, episode_desc, episode_duration, episode_release_date = row
        episode_duration = episode_duration or 0

        episodes.append({
            "id_episode": episode_id,
            "judul_episode": episode_title,
            "deskripsi_episode": episode_desc,
            "durasi_episode": format_durasi(episode_duration),
            "tanggal_rilis_episode": episode_release_date,
        })

    content = {
        "podcast_title": podcast_title,
        "episodes": episodes
    }

    return render(request, 'list_episode.html', content)