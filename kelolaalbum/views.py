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


@connectdb
def list_album(cursor: CursorWrapper, request):
    email = request.session["email"]
    # try:
    #     email = request.session.get('email')
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    if (request.session["role"] == "label"):
        cursor.execute("Set search_path to marmut;")
        query =(rf"""SELECT album.judul AS judul_album, label.nama AS label, album.jumlah_lagu AS jumlah_lagu, album.total_durasi AS total_durasi, album.id AS id_album
                    FROM album
                    JOIN label ON album.id_label = label.id
                    JOIN song ON album.id = song.id_album
                    JOIN artist ON song.id_artist = artist.id
                    JOIN akun ON artist.email_akun = akun.email
                    WHERE label.email = '{email}'
                    GROUP BY album.judul, label.nama, album.jumlah_lagu, album.total_durasi, album.id;
                                """)
    else:
        cursor.execute("Set search_path to marmut;")
        query =(rf"""SELECT album.judul AS judul_album, label.nama AS label, album.jumlah_lagu AS jumlah_lagu, album.total_durasi AS total_durasi, album.id AS id_album
                    FROM album
                    JOIN song ON album.id = song.id_album
                    JOIN artist ON song.id_artist = artist.id
                    JOIN akun ON artist.email_akun = akun.email
                    JOIN label ON album.id_label = label.id
                    WHERE akun.email = '{email}'
                    GROUP BY album.judul, akun.nama, label.nama, album.jumlah_lagu, album.total_durasi, album.id;
                                """)
    cursor.execute(query)
    result = cursor.fetchall()
    albums = []
    for row in result:
        durasi = row[3]
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
            "id":row[4]
        })
    email = request.session["email"]
    role = request.session["role"]

    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        if (role == "pengguna") :
            cursor.execute(f"SELECT * FROM AKUN WHERE email = '{email}'")
        else:
            cursor.execute(f"SELECT * FROM LABEL WHERE email = '{email}'")
        user_data = cursor.fetchone()

        if not user_data:
            return redirect('authentication:login')

        cursor.execute(f"SELECT * FROM PREMIUM WHERE email = '{email}'")
        premium = cursor.fetchone()
        if premium:
            is_premium = True
        else:
            is_premium = False

        cursor.execute("set search_path to public")

    roles = get_role_pengguna(email)
    return render(request, 'list_album_songwriter_artist.html', {'albums' : albums, 'is_logged_in': True,
                                                                'user': user_data,
                                                                'role': role,
                                                                'roles': roles,
                                                                'is_premium': is_premium})

@connectdb
@csrf_exempt
def create_album(cursor: CursorWrapper, request):
    email = request.session["email"]
    if request.method == 'POST':
        judul_album = request.POST['judul_album']
        id_label = request.POST['label']
        selected_songs = request.POST.getlist('songs')  # Get the selected songs
        id_album = uuid.uuid4()
        judul = request.POST.get('judul')
        durasi = int(request.POST.get('durasi'))
        id = str(uuid.uuid4())
        
        cursor.execute("""
                        SET search_path to marmut;
                        INSERT INTO album (id, judul, jumlah_lagu, total_durasi, id_label)
                        VALUES (%s, %s, %s, %s, %s);
                        """, [id_album, judul_album, len(selected_songs), 0, id_label])
        
        # Insert songs into the album        
        query = """
                SET search_path to marmut;
                INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
                VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s);
                """
        
        query3 = """
                SET search_path to marmut;
                select id from artist where email_akun= %s
                """

        query2 =    """
                SET search_path to marmut;
                INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download)
                VALUES (%s, %s, %s, %s, %s);
                    """
        with connection.cursor() as cursor:
            cursor.execute(query3, email)
            id_artist = cursor.fetchall()
            cursor.execute(query, [id, judul, 2024, durasi])
            cursor.execute(query2, [id, id_artist[0], id_album, 0, 0])

        
        return redirect('/kelolaalbum/list-album/')

    # Fetch labels for dropdown
    cursor.execute("Set search_path to marmut;")
    cursor.execute("SELECT id, nama FROM label")
    labels = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
                       SET search_path to marmut; 
                       SELECT distinct genre 
                       FROM genre;
                       """)
        genres = cursor.fetchall()
        cursor.execute("SET search_path to marmut; SELECT email_akun FROM songwriter;")
        songwriters = cursor.fetchall()
        cursor.execute("SET search_path to marmut; SELECT email_akun FROM songwriter;")
        artists = cursor.fetchall()
        
    email = request.session["email"]
    role = request.session["role"]

    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        if (role == "pengguna") :
            cursor.execute(f"SELECT * FROM AKUN WHERE email = '{email}'")
        else:
            cursor.execute(f"SELECT * FROM LABEL WHERE email = '{email}'")
        user_data = cursor.fetchone()
        if not user_data:
            return redirect('authentication:login')
        cursor.execute(f"SELECT * FROM PREMIUM WHERE email = '{email}'")
        premium = cursor.fetchone()
        if premium:
            is_premium = True
        else:
            is_premium = False
        cursor.execute("set search_path to public")

    roles = get_role_pengguna(email)
    return render(request, 'create_album.html', {'labels': labels, 
                                                'songwriters' : songwriters,
                                                'genres': genres, 
                                                'artists': artists, 
                                                'roles': roles,
                                                'is_logged_in': True,
                                                'user': user_data,
                                                'role': role,
                                                'roles': roles,
                                                'is_premium': is_premium})


def list_song_album(request, album_id):
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        query = ("""
                SELECT k.judul, k.durasi, s.total_play, s.total_download, s.id_konten
                FROM song s
                JOIN konten k ON s.id_konten = k.id
                JOIN artist a ON s.id_artist = a.id
                WHERE s.id_album = %s;
                """)
    with connection.cursor() as cursor:    
        cursor.execute(query, [album_id])
        result = cursor.fetchall()
        songs = []
        for row in result:
            durasi = row[1]
            durasi_jam = durasi // 60
            durasi_menit = durasi % 60
            if durasi_jam == 0:
                durasi = str(durasi_menit) + " menit"
            else:
                durasi = str(durasi_jam) + " jam " + str(durasi_menit) + " menit"
            songs.append({
                "judul": row[0],
                "durasi": durasi,
                "total_play": row[2],
                "total_download": row[3],
                "id": row[4]
            })
    with conn.cursor() as cursor:
        cursor.execute("set search_path to public")
    email = request.session["email"]
    role = request.session["role"]

    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        if (role == "pengguna") :
            cursor.execute(f"SELECT * FROM AKUN WHERE email = '{email}'")
        else:
            cursor.execute(f"SELECT * FROM LABEL WHERE email = '{email}'")
        user_data = cursor.fetchone()

        if not user_data:
            return redirect('authentication:login')

        cursor.execute(f"SELECT * FROM PREMIUM WHERE email = '{email}'")
        premium = cursor.fetchone()
        if premium:
            is_premium = True
        else:
            is_premium = False

        cursor.execute("set search_path to public")

    roles = get_role_pengguna(email)
    return render(request, 'list_song.html', {'songs' : songs, 
                                              'roles': roles,
                                                'is_logged_in': True,
                                                'user': user_data,
                                                'role': role,
                                                'roles': roles,
                                                'is_premium': is_premium})

def delete_album(request, album_id):
    query = """
            SET search_path to marmut;
            DELETE FROM ALBUM
            WHERE id = %s;
            """
    
    with connection.cursor() as cursor:
            cursor.execute(query, [album_id])

    return redirect('/kelolaalbum/list-album/')

def delete_song(request, song_id,):
    query = """
            SET search_path to marmut;
            DELETE FROM SONG
            WHERE id_konten = %s;
            """
    
    with connection.cursor() as cursor:
            cursor.execute(query, [song_id])

    return redirect('/kelolaalbum/list-album/')


from django.db import connection as conn
def get_role_pengguna(email: str) -> list:
    roles = []
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        cursor.execute(f"SELECT * FROM ARTIST WHERE email_akun = '{email}'")
        artist = cursor.fetchall()
        cursor.execute(f"SELECT * FROM SONGWRITER WHERE email_akun = '{email}'")
        songwriter = cursor.fetchall()
        cursor.execute(f"SELECT * FROM PODCASTER WHERE email = '{email}'")
        podcaster = cursor.fetchall()
        cursor.execute("set search_path to public")
    if len(artist) > 0:
        roles.append("Artist")
    if len(songwriter) > 0:
        roles.append("Songwriter")
    if len(podcaster) > 0:
        roles.append("Podcaster")
    
    return roles