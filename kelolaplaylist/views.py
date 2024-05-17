from django.shortcuts import render

# Create your views here.
import uuid
from django.db import connection
from django.shortcuts import render, redirect
from datetime import date

email_pembuat = 'angela93@hotmail.com'

def kelolaplaylist(request):
    if request.method == 'POST':
        judul_playlist = request.POST['judul_playlist']
        deskripsi_playlist = request.POST['deskripsi_playlist']
        id_user_playlist = uuid.uuid4()
        id_playlist = id_user_playlist

        with connection.cursor() as cursor:
            cursor.execute("Set search_path to marmut;")
            cursor.execute("""
                            INSERT INTO playlist (
                                id
                            )
                            VALUES (%s)
                            """, [id_playlist])
            
            cursor.execute("""
                           INSERT INTO user_playlist (
                                email_pembuat, 
                                id_user_playlist, 
                                judul, 
                                deskripsi, 
                                jumlah_lagu, 
                                tanggal_dibuat, 
                                id_playlist, 
                                total_durasi
                           )
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                           """, [email_pembuat, id_user_playlist, judul_playlist, deskripsi_playlist, 0, date.today(), id_playlist, 0])
            
            return redirect('/kelolaplaylist/')
            
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        SELECT judul, jumlah_lagu, total_durasi, id_user_playlist
                        FROM user_playlist
                        WHERE email_pembuat = %s;
                        """, [email_pembuat])
        result = cursor.fetchall()
        playlists = []
        for row in result:
            durasi = row[2]
            durasi_jam = durasi // 60
            durasi_menit = durasi % 60
            if durasi_jam == 0:
                durasi = str(durasi_menit) + " menit"
            else:
                durasi = str(durasi_jam) + " jam " + str(durasi_menit) + " menit"
            playlists.append({
                'id': row[3],
                'judul': row[0],
                'jumlah_lagu': row[1],
                'total_durasi': durasi
            })

    return render(request, 'kelola_playlist.html', {
        'playlists': playlists
    })

def editplaylist(request, id_playlist):
    if request.method == 'POST':
        judul_playlist = request.POST['judul_playlist']
        deskripsi_playlist = request.POST['deskripsi_playlist']

        with connection.cursor() as cursor:
            cursor.execute("Set search_path to marmut;")
            cursor.execute("""
                            UPDATE user_playlist
                            SET judul = %s, deskripsi = %s
                            WHERE id_user_playlist = %s;
                            """, [judul_playlist, deskripsi_playlist, id_playlist])
            
            return redirect('/kelolaplaylist/')
        
    judul_playlist = ''
    deskripsi_playlist = ''
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        SELECT judul, deskripsi
                        FROM user_playlist
                        WHERE id_user_playlist = %s;
                        """, [id_playlist])
        result = cursor.fetchall()
        judul_playlist, deskripsi_playlist = result[0]

    return render(request, 'edit_playlist.html', {
        'id': id_playlist,
        'judul': judul_playlist,
        'deskripsi': deskripsi_playlist
    })

def deleteplaylist(request, id_playlist):
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
                        DELETE FROM user_playlist
                        WHERE id_user_playlist = %s;
                        """, [id_playlist])
        
    return redirect('/kelolaplaylist/')