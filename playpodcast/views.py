from django.shortcuts import render
from django.db import connection


def podcast_detail(request, podcast_id):
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
            WHERE p.id_konten = %s
            ORDER BY k.judul, e.tanggal_rilis;
            """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [podcast_id])
        rows = cursor.fetchall()

    podcasts_dict = {}
    for row in rows:
        podcast_id, podcast_title, episode_id, episode_title, episode_desc, episode_duration, episode_release_date, genre, podcaster_name = row
        
        if podcast_id not in podcasts_dict:
            podcasts_dict[podcast_id] = {
                "judul_podcast": podcast_title,
                "genres": set(),
                "nama_podcaster": podcaster_name,
                "total_durasi": 0,
                "episodes": [],
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

        if genre:
            podcasts_dict[podcast_id]["genres"].add(genre)

    for podcast in podcasts_dict.values():
        podcast["total_durasi"] = format_durasi(podcast["total_durasi"])
        podcast["genres"] = ", ".join(podcast["genres"])

    content = {"podcasts": list(podcasts_dict.values())}

    return render(request, 'podcast_detail.html', content)
    
def format_durasi(minutes):
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours} hour {mins} minutes"
    elif hours > 0:
        return f"{hours} hour"
    else:
        return f"{mins} minutes"