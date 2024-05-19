from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import json
from django.http import JsonResponse

def chart_list(request):
    query = """
            SET SEARCH_PATH TO MARMUT;
            SELECT tipe, id_playlist
            FROM CHART;
            """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        charts = cursor.fetchall()

    chart_data = [
        {
            'name': chart[0],
            'id': chart[1]
        } for chart in charts
    ]

    context = {
        'charts': chart_data
    }
    return render(request, 'chart_list.html', context)

def chart_detail(request, id, tipe):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    # email = request.session["email"]
    # role = request.session["role"]
    # roles = get_role_pengguna(email)

    query = """
            SET SEARCH_PATH TO MARMUT;
            DELETE FROM PLAYLIST_SONG 
            WHERE id_playlist=%s;
            """
    query2 =    """
                SET SEARCH_PATH TO MARMUT;
                INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
                SELECT DISTINCT %s::uuid, subquery.id_konten
                FROM (
                    SELECT id_konten, total_play
                    FROM SONG
                    WHERE total_play > 0
                    ORDER BY total_play DESC
                    LIMIT 20
                ) AS subquery;
                """
    
    query3 =    """
                SET SEARCH_PATH TO MARMUT;
                SELECT DISTINCT K.judul, A.nama, K.tanggal_rilis, S.total_play, K.id
                FROM AKUN A
                JOIN PLAYLIST_SONG P ON P.id_playlist = %s
                JOIN ARTIST R ON R.email_akun = A.email
                JOIN SONG S ON S.id_konten = P.id_song
                JOIN KONTEN K ON K.id = P.id_song
                WHERE S.id_artist = R.id
                ORDER BY S.total_play DESC;
                """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [id])
        cursor.execute(query2, [id])
        cursor.execute(query3, [id])
        searched_table = cursor.fetchall()

    all_table = []
    for i in searched_table:
        song = {}
        song["judul"] = i[0]
        song["nama"] = i[1]
        song["tanggal_rilis"] = i[2]
        song["total_play"] = i[3]
        song["id"] = str(i[4])
        all_table.append(song)

    context = {
        # 'is_logged_in': True,
        # 'role': role,
        # 'roles': roles,
        'tipe': tipe,
        # 'is_premium': check_premium(email),
        'data_table': all_table
    }

    return render(request, "chart_detail.html", context)