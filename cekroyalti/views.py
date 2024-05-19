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

email = 'jennifersutton@gmail.com'

@connectdb
def list_royalti(cursor: CursorWrapper, request):
    # try:
    #     email = request.session.get('email')
    # except:
    #     return HttpResponseRedirect(reverse("authentication:login_user"))
    cursor.execute("Set search_path to marmut;")
    query =(rf"""SELECT s.id_konten AS "ID",
                k.judul AS "Judul Lagu",
                a.judul AS "Judul Album",
                s.total_play AS "Total Play",
                s.total_download AS "Total Download",
                COALESCE(SUM(r.jumlah), 0) AS "Total Royalti Didapat"
            FROM marmut.song s
                JOIN marmut.konten k ON s.id_konten = k.id
                LEFT JOIN marmut.album a ON s.id_album = a.id
                LEFT JOIN marmut.royalti r ON s.id_konten = r.id_song
            WHERE
                s.id_artist IN (
                    SELECT id FROM marmut.artist WHERE email_akun = '{email}'
                )
                OR s.id_album IN (
                    SELECT id FROM marmut.label WHERE email = '{email}'
                )
                OR s.id_konten IN (
                    SELECT id_song FROM marmut.songwriter_write_song WHERE id_songwriter IN (
                        SELECT id FROM marmut.songwriter WHERE email_akun = '{email}'
                    )
                )
            GROUP BY s.id_konten,
                k.judul,
                a.judul,
                s.total_play,
                s.total_download
            ORDER BY k.judul;
            """)
    cursor.execute(query)
    result = cursor.fetchall()
    royalti = []
    for row in result:
        royalti.append({
            "judul": row[1],
            "judul_album": row[2],
            "total_play": row[3],
            "total_download": row[4],
            "total_royalti":row[5]
        })
    return render(request, 'cek_royalti.html', {'royaltis' : royalti})
