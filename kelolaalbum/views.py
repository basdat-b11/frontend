from django.shortcuts import render

# Create your views here.
import uuid
from django.urls import reverse
from django.db import connection
from django.shortcuts import render, redirect
from datetime import date
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponseRedirect
from utils.query import connectdb
from django.views.decorators.csrf import csrf_exempt

email = 'robyn54@yahoo.com'

@connectdb
def list_album(cursor: CursorWrapper, request):
    # try:
    #     email = request.session.get('email')
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    cursor.execute("Set search_path to marmut;")
    query =(rf"""SELECT album.judul AS judul_album, label.nama AS label, album.jumlah_lagu AS jumlah_lagu, album.total_durasi AS total_durasi
                FROM album
                JOIN song ON album.id = song.id_album
                JOIN artist ON song.id_artist = artist.id
                JOIN akun ON artist.email_akun = akun.email
                JOIN label ON album.id_label = label.id
                WHERE akun.email = '{email}'
                GROUP BY album.judul, akun.nama, label.nama, album.jumlah_lagu, album.total_durasi;
                                """)
    cursor.execute(query)
    result = cursor.fetchall()
    print (result)
    albums = []
    for row in result:
        durasi = row[2]
        durasi_jam = durasi // 60
        durasi_menit = durasi % 60
        if durasi_jam == 0:
            durasi = str(durasi_menit) + " menit"
        else:
            durasi = str(durasi_jam) + " jam " + str(durasi_menit) + " menit"
        albums.append({
            "judul": row[0],
            "label": row[1],
            "jumlah_lagu": row[2],
            "total_durasi": durasi,
        })
    print (result)
    return render(request, 'list_album_songwriter_artist.html', {'albums' : albums})

@connectdb
@csrf_exempt
def create_album(cursor: CursorWrapper, request):
    if request.method == 'POST':
        judul_album = request.POST['judul_album']
        id_label = request.POST['label']
        selected_songs = request.POST.getlist('songs')  # Get the selected songs
        id_album = uuid.uuid4()
        
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        INSERT INTO album (id, judul, jumlah_lagu, total_durasi, id_label)
                        VALUES (%s, %s, %s, %s, %s)
                        """, [id_album, judul_album, len(selected_songs), 0, id_label])
        
        # Insert songs into the album
        for song_id in selected_songs:
            cursor.execute("""
                           INSERT INTO song_album (id_song, id_album)
                           VALUES (%s, %s)
                           """, [song_id, id_album])
        
        return redirect('/main/kelolaalbum/list-album/')

    # Fetch labels for dropdown
    cursor.execute("Set search_path to marmut;")
    cursor.execute("SELECT id, nama FROM label")
    labels = cursor.fetchall()

    cursor.execute("""
                   SELECT song.id_konten, song.judul
                   FROM song
                   JOIN artist ON song.id_artist = artist.id
                   JOIN akun ON artist.email_akun = akun.email
                   WHERE akun.email = %s
                   """, [email])
    songs = cursor.fetchall()
    
    return render(request, 'create_album.html', {'labels': labels, 'songs': songs})