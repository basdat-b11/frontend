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
    albums = cursor.fetchall()
    print (albums)
    
    context = {
        "judul": albums[0][0],
        "label": albums[0][1],
        "jumlah_lagu": albums[0][2],
        "total_durasi": albums[0][3],
    }

    return render(request, 'list_album_songwriter_artist.html', context)