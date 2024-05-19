from django.shortcuts import render, redirect
from django.db import connection
import uuid

def create_song_artist(request, album_id):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        durasi = int(request.POST.get('durasi'))
        id = str(uuid.uuid4())

        query = """
                SET search_path to marmut;
                INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
                VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s);
                """
        
        query3 = """
                SET search_path to marmut;
                select id from artist where email_akun='davidmoore@yahoo.com'
                """

        query2 =    """
                SET search_path to marmut;
                INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download)
                VALUES (%s, %s, %s, %s, %s);
                    """
        with connection.cursor() as cursor:
            cursor.execute(query3)
            id_artist = cursor.fetchall()
            cursor.execute(query, [id, judul, 2024, durasi])
            cursor.execute(query2, [id, id_artist[0], album_id, 0, 0])

        return redirect('/main/kelolaalbum/list-album/')  # Adjust the redirect as needed
    
    with connection.cursor() as cursor:
        cursor.execute("""
                SET search_path to marmut; 
                SELECT distinct genre 
                FROM genre;
                """)
        genres = cursor.fetchall()
        cursor.execute("SET search_path to marmut; SELECT email_akun FROM songwriter;")
        songwriters = cursor.fetchall()

    context = {
        'album_id': album_id,
        'songwriters': songwriters,
        'genres' : genres
    }

    return render(request, 'create_song.html', context)