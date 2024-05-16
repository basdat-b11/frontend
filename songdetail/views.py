from django.db import connection
from django.shortcuts import render

def song_detail(request):
    judul_lagu = 'Many production choice choice'
    genres = []
    artist = ''
    songwriters = []
    durasi, tanggal_rilis, tahun, total_play, total_download, album = "", "", "", "", "", ""

    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                       SELECT genre
                       FROM genre
                       JOIN konten ON genre.id_konten = konten.id
                       WHERE konten.judul = %s;
                       """, [judul_lagu])
        result = cursor.fetchall()
        for row in result:
            genres.append(row[0])

        cursor.execute("""
                       SELECT akun.nama
                       FROM artist
                       JOIN akun ON artist.email_akun = akun.email
                       JOIN song ON artist.id = song.id_artist
                       JOIN konten ON song.id_konten = konten.id
                       WHERE konten.judul = %s;
                       """, [judul_lagu])
        result = cursor.fetchall()
        artist = result[0][0]

        cursor.execute("""
                       SELECT akun.nama
                       FROM songwriter
                          JOIN akun ON songwriter.email_akun = akun.email
                            JOIN songwriter_write_song ON songwriter.id = songwriter_write_song.id_songwriter
                            JOIN song ON songwriter_write_song.id_song = song.id_konten
                            JOIN konten ON song.id_konten = konten.id
                            WHERE konten.judul = %s;
                          """, [judul_lagu])
        result = cursor.fetchall()
        for row in result:
            songwriters.append(row[0])

        cursor.execute("""
                        SELECT 
                            konten.durasi, 
                            konten.tanggal_rilis, 
                            konten.tahun, 
                            song.total_play, 
                            song.total_download, 
                            album.judul
                        FROM song
                        JOIN konten ON song.id_konten = konten.id
                        JOIN album ON song.id_album = album.id
                        WHERE konten.judul = %s;
                        """, [judul_lagu])
        result = cursor.fetchall()
        durasi, tanggal_rilis, tahun, total_play, total_download, album = result[0]
    
    return render(request, 'song_detail.html', {
        'judul_lagu': judul_lagu,
        'genres': genres,
        'artist': artist,
        'songwriters': songwriters,
        'durasi': durasi,
        'tanggal_rilis': tanggal_rilis,
        'tahun': tahun,
        'total_play': total_play,
        'total_download': total_download,
        'album': album
    })