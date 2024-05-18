from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

def playlist(request, id_user_playlist):
    judul_playlist = ''
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        SELECT judul
                        FROM user_playlist
                        WHERE id_user_playlist = %s;
                        """, [id_user_playlist])
        result = cursor.fetchall()
        judul_playlist = result[0][0]

    result = ""
    judul, pembuat, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi = "", "", "", "", "", ""
    id_playlist = ""
    daftar_lagu = []
    pilihan_lagu = []
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                       SELECT judul, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi 
                       FROM user_playlist
                       WHERE id_user_playlist = %s;
                        """, [id_user_playlist])
        result = cursor.fetchall()
        judul, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi = result[0]

        cursor.execute("""
                       SELECT akun.nama, id_playlist
                       FROM user_playlist
                       JOIN akun ON user_playlist.email_pembuat = akun.email
                       WHERE id_user_playlist = %s;
                        """, [id_user_playlist])
        result = cursor.fetchall()
        pembuat = result[0][0]
        id_playlist = result[0][1]

        cursor.execute("""
                        SELECT konten.judul, akun.nama, durasi, song.id_konten
                        FROM playlist_song
                        JOIN song ON playlist_song.id_song = song.id_konten
                        JOIN playlist ON playlist_song.id_playlist = playlist.id
                        JOIN konten ON song.id_konten = konten.id
                        JOIN artist ON song.id_artist = artist.id
                        JOIN akun ON artist.email_akun = akun.email
                        JOIN user_playlist ON playlist.id = user_playlist.id_playlist
                        WHERE id_user_playlist = %s;
                        """, [id_user_playlist])
        
        result = cursor.fetchall()
        for row in result:
            durasi = row[2]
            durasi_jam = durasi // 60
            durasi_menit = durasi % 60
            if durasi_jam == 0:
                durasi = str(durasi_menit) + " menit"
            else:
                durasi = str(durasi_jam) + " jam " + str(durasi_menit) + " menit"
            daftar_lagu.append({
                'judul': row[0],
                'artist': row[1],
                'durasi': durasi,
                'id': row[3]
            })

        cursor.execute("""
                        SELECT konten.id, judul, akun.nama
                        FROM song
                        JOIN konten ON song.id_konten = konten.id
                        JOIN artist ON song.id_artist = artist.id
                        JOIN akun ON artist.email_akun = akun.email
                        WHERE song.id_konten NOT IN (
                            SELECT id_song
                            FROM playlist_song
                            WHERE id_playlist = %s
                        );
                        """, [id_playlist])
        result = cursor.fetchall()
        for row in result:
            pilihan_lagu.append({
                'id': row[0],
                'judul': row[1],
                'artist': row[2]
            })

    # print(result)
    # print("Judul: ", judul)
    # print("Jumlah lagu: ", jumlah_lagu)
    # print("Total durasi: ", total_durasi)
    # print("Tanggal dibuat: ", tanggal_dibuat)
    # print("Deskripsi: ", deskripsi)

    total_durasi_jam = total_durasi // 60
    total_durasi_menit = total_durasi % 60
    if total_durasi_jam == 0:
        total_durasi = str(total_durasi_menit) + " menit"
    else: 
        total_durasi = str(total_durasi_jam) + " jam " + str(total_durasi_menit) + " menit"

    return render(request, 'play_user_playlist.html', {
        'id_user_playlist': id_user_playlist,
        'id_playlist': id_playlist,
        'judul': judul,
        'pembuat': pembuat,
        'jumlah_lagu': jumlah_lagu,
        'total_durasi': total_durasi,
        'tanggal_dibuat': tanggal_dibuat,
        'deskripsi': deskripsi,
        'daftar_lagu': daftar_lagu,
        'pilihan_lagu': pilihan_lagu
    })

def tambahlagu(request, id_user_playlist):
    id_lagu = request.POST['id_lagu']
    is_api = request.POST.get('is_api', False)

    print("ID Playlist: ", id_user_playlist)

    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        INSERT INTO playlist_song (id_playlist, id_song)
                        VALUES (%s, %s);
                        """, [id_user_playlist, id_lagu])
        
        jumlah_lagu = 0
        total_durasi = 0
        cursor.execute("""
                        SELECT COUNT(*), SUM(durasi)
                        FROM playlist_song
                        JOIN song ON playlist_song.id_song = song.id_konten
                        JOIN konten ON song.id_konten = konten.id
                        WHERE id_playlist = %s;
                        """, [id_user_playlist])
        result = cursor.fetchall()
        jumlah_lagu, total_durasi = result[0]

        cursor.execute("""
                        UPDATE user_playlist
                        SET jumlah_lagu = %s, total_durasi = %s
                        WHERE id_user_playlist = %s;
                        """, [jumlah_lagu, total_durasi, id_user_playlist])
        
    if is_api:
        return JsonResponse({'status': 'success'})

    previous_page = request.META.get('HTTP_REFERER')

    return HttpResponseRedirect(previous_page)


#                         Table "marmut.user_playlist"
#       Column      |          Type          | Collation | Nullable | Default
# ------------------+------------------------+-----------+----------+---------
#  email_pembuat    | character varying(50)  |           | not null |
#  id_user_playlist | uuid                   |           | not null |
#  judul            | character varying(100) |           | not null |
#  deskripsi        | character varying(500) |           | not null |
#  jumlah_lagu      | integer                |           | not null |
#  tanggal_dibuat   | date                   |           | not null |
#  id_playlist      | uuid                   |           |          |
#  total_durasi     | integer                |           | not null | 0
# Indexes:
#     "user_playlist_pkey" PRIMARY KEY, btree (email_pembuat, id_user_playlist)
# Foreign-key constraints:
#     "user_playlist_email_pembuat_fkey" FOREIGN KEY (email_pembuat) REFERENCES akun(email) ON UPDATE CASCADE ON DELETE CASCADE
#     "user_playlist_id_playlist_fkey" FOREIGN KEY (id_playlist) REFERENCES playlist(id) ON UPDATE CASCADE ON DELETE CASCADE
# Referenced by:
#     TABLE "akun_play_user_playlist" CONSTRAINT "akun_play_user_playlist_id_user_playlist_email_pembuat_fkey" FOREIGN KEY (id_user_playlist, email_pembuat) REFERENCES user_playlist(id_user_playlist, email_pembuat) ON UPDATE CASCADE ON DELETE CASCADE

#             Table "marmut.playlist"
#  Column | Type | Collation | Nullable | Default
# --------+------+-----------+----------+---------
#  id     | uuid |           | not null |
# Indexes:
#     "playlist_pkey" PRIMARY KEY, btree (id)
# Referenced by:
#     TABLE "chart" CONSTRAINT "chart_id_playlist_fkey" FOREIGN KEY (id_playlist) REFERENCES playlist(id) ON UPDATE CASCADE ON DELETE CASCADE
#     TABLE "playlist_song" CONSTRAINT "playlist_song_id_playlist_fkey" FOREIGN KEY (id_playlist) REFERENCES playlist(id) ON UPDATE CASCADE ON DELETE CASCADE
#     TABLE "user_playlist" CONSTRAINT "user_playlist_id_playlist_fkey" FOREIGN KEY (id_playlist) REFERENCES playlist(id) ON UPDATE CASCADE ON DELETE CASCADE

#             Table "marmut.playlist_song"
#    Column    | Type | Collation | Nullable | Default
# -------------+------+-----------+----------+---------
#  id_playlist | uuid |           | not null |
#  id_song     | uuid |           | not null |
# Indexes:
#     "playlist_song_pkey" PRIMARY KEY, btree (id_playlist, id_song)
# Foreign-key constraints:
#     "playlist_song_id_playlist_fkey" FOREIGN KEY (id_playlist) REFERENCES playlist(id) ON UPDATE CASCADE ON DELETE CASCADE
#     "playlist_song_id_song_fkey" FOREIGN KEY (id_song) REFERENCES song(id_konten) ON UPDATE CASCADE ON DELETE CASCADE

#                     Table "marmut.song"
#      Column     |  Type   | Collation | Nullable | Default
# ----------------+---------+-----------+----------+---------
#  id_konten      | uuid    |           | not null |
#  id_artist      | uuid    |           |          |
#  id_album       | uuid    |           |          |
#  total_play     | integer |           | not null | 0
#  total_download | integer |           | not null | 0
# Indexes:
#     "song_pkey" PRIMARY KEY, btree (id_konten)
# Foreign-key constraints:
#     "song_id_album_fkey" FOREIGN KEY (id_album) REFERENCES album(id) ON UPDATE CASCADE ON DELETE CASCADE
#     "song_id_artist_fkey" FOREIGN KEY (id_artist) REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE
#     "song_id_konten_fkey" FOREIGN KEY (id_konten) REFERENCES konten(id) ON UPDATE CASCADE ON DELETE CASCADE
# Referenced by:
#     TABLE "akun_play_song" CONSTRAINT "akun_play_song_id_song_fkey" FOREIGN KEY (id_song) REFERENCES song(id_konten) ON UPDATE CASCADE ON DELETE CASCADE
#     TABLE "downloaded_song" CONSTRAINT "downloaded_song_id_song_fkey" FOREIGN KEY (id_song) REFERENCES song(id_konten) ON UPDATE CASCADE ON DELETE CASCADE
#     TABLE "playlist_song" CONSTRAINT "playlist_song_id_song_fkey" FOREIGN KEY (id_song) REFERENCES song(id_konten) ON UPDATE CASCADE ON DELETE CASCADE
#     TABLE "royalti" CONSTRAINT "royalti_id_song_fkey" FOREIGN KEY (id_song) REFERENCES song(id_konten) ON UPDATE CASCADE ON DELETE CASCADE
#     TABLE "songwriter_write_song" CONSTRAINT "songwriter_write_song_id_song_fkey" FOREIGN KEY (id_song) REFERENCES song(id_konten) ON UPDATE CASCADE ON DELETE CASCADE