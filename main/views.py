from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
import json

# Create your views here.
def test_akun(request):
    result = ""
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("SELECT * FROM akun;")
        result = cursor.fetchall()
    
    print(result)
    return HttpResponse(result, content_type='application/json', status=200)

def kelola_playlist(request):
    return render(request, 'kelola_playlist.html')

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

def playlist(request):
    judul_playlist = 'Model despite husband'

    result = ""
    judul, pembuat, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi = "", "", "", "", "", ""
    daftar_lagu = []
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                       SELECT judul, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi 
                       FROM user_playlist
                       WHERE judul = %s;
                       """, [judul_playlist])
        result = cursor.fetchall()
        judul, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi = result[0]

        cursor.execute("""
                       SELECT judul, nama
                       FROM user_playlist
                       JOIN akun ON user_playlist.email_pembuat = akun.email
                       WHERE judul = %s;
                       """, [judul_playlist])
        result = cursor.fetchall()
        pembuat = result[0][0]

        cursor.execute("""
                       SELECT konten.judul, akun.nama, konten.durasi
                       FROM user_playlist
                       JOIN playlist_song ON user_playlist.id_playlist = playlist_song.id_playlist
                       JOIN song ON playlist_song.id_song = song.id_konten
                       JOIN artist ON song.id_artist = artist.id
                       JOIN akun ON artist.email_akun = akun.email
                       JOIN konten ON song.id_konten = konten.id
                       WHERE user_playlist.judul = %s;
                        """, [judul_playlist])
        result = cursor.fetchall()
        for row in result:
            daftar_lagu.append({
                'judul': row[0],
                'artist': row[1],
                'durasi': row[2]
            })

        print("daftar_lagu", daftar_lagu)

    # print(result)
    # print("Judul: ", judul)
    # print("Jumlah lagu: ", jumlah_lagu)
    # print("Total durasi: ", total_durasi)
    # print("Tanggal dibuat: ", tanggal_dibuat)
    # print("Deskripsi: ", deskripsi)

    total_durasi_jam = total_durasi // 60
    total_durasi_menit = total_durasi % 60
    total_durasi = str(total_durasi_jam) + " jam " + str(total_durasi_menit) + " menit"

    return render(request, 'play_user_playlist.html', {
        'judul': judul,
        'pembuat': pembuat,
        'jumlah_lagu': jumlah_lagu,
        'total_durasi': total_durasi,
        'tanggal_dibuat': tanggal_dibuat,
        'deskripsi': deskripsi,
        'daftar_lagu': daftar_lagu
    })
