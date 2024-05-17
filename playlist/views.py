from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

def playlist(request, id_playlist):
    judul_playlist = ''
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        SELECT judul
                        FROM user_playlist
                        WHERE id_user_playlist = %s;
                        """, [id_playlist])
        result = cursor.fetchall()
        judul_playlist = result[0][0]

    result = ""
    judul, pembuat, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi = "", "", "", "", "", ""
    daftar_lagu = []
    pilihan_lagu = []
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
                       SELECT akun.nama
                       FROM user_playlist
                       JOIN akun ON user_playlist.email_pembuat = akun.email
                       WHERE judul = %s;
                       """, [judul_playlist])
        result = cursor.fetchall()
        pembuat = result[0][0]

        cursor.execute("""
                       SELECT konten.judul, akun.nama, konten.durasi, konten.id
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

def tambahlagu(request, id_playlist):
    id_lagu = request.POST['id_lagu']
    is_api = request.POST.get('is_api', False)

    print("ID Playlist: ", id_playlist)

    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        INSERT INTO playlist_song (id_playlist, id_song)
                        VALUES (%s, %s);
                        """, [id_playlist, id_lagu])
        
        jumlah_lagu = 0
        total_durasi = 0
        cursor.execute("""
                        SELECT COUNT(*), SUM(durasi)
                        FROM playlist_song
                        JOIN song ON playlist_song.id_song = song.id_konten
                        JOIN konten ON song.id_konten = konten.id
                        WHERE id_playlist = %s;
                        """, [id_playlist])
        result = cursor.fetchall()
        jumlah_lagu, total_durasi = result[0]

        cursor.execute("""
                        UPDATE user_playlist
                        SET jumlah_lagu = %s, total_durasi = %s
                        WHERE id_user_playlist = %s;
                        """, [jumlah_lagu, total_durasi, id_playlist])
        
    if is_api:
        return JsonResponse({'status': 'success'})

    previous_page = request.META.get('HTTP_REFERER')

    return HttpResponseRedirect(previous_page)