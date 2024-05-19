from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection as conn
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from utils.query import query
import random
import uuid

def logout(request):
    request.session.flush()
    request.session.clear_expired()

    context = {
        "is_logged_in": False
    }
    return render(request, "LoginRegister.html", context)

def show_landingpage(request):
    context = {
        "is_logged_in": False
    }
    return render(request, "LoginRegister.html", context)

@csrf_exempt
def login(request):
    if "email" in request.session:
        return redirect('authentication:dashboard')
    context = {
        "is_logged_in": False
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        with conn.cursor() as cursor:
            cursor.execute("set search_path to marmut")
            cursor.execute(f"SELECT * FROM AKUN WHERE email = '{email}' AND password = '{password}'")
            user_pengguna = cursor.fetchone()
            cursor.execute(f"SELECT * FROM LABEL WHERE email = '{email}' AND password = '{password}'")
            user_label = cursor.fetchone()

            if not user_pengguna and not user_label:
                context["message"] = "Email atau Password Salah"
                return render(request, "login.html", context)
            
            cursor.execute("set search_path to public")
            request.session["email"] = email
            if user_pengguna:
                request.session["role"] = "pengguna"
            elif user_label:
                request.session["role"] = "label"
            return dashboard(request)
            
    return render(request, "login.html", context)

def dashboard(request):
    if "email" not in request.session:
        return redirect('authentication:login')

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
    context = {
        'is_logged_in': True,
        'user': user_data,
        'role': role,
        'roles': roles,
        'is_premium': is_premium
    }
    if ("Artist" in roles and "Songwriter" in roles):
        context['songs'] = get_songs_artist_songwriter(email)

    return render(request, 'Dashboard.html', context)


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

def get_songs_artist_songwriter(email: str) -> list:
    songs = []
    formatted_songs = []
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        cursor.execute(f"SELECT id FROM ARTIST WHERE email_akun = '{email}'")
        id_json = cursor.fetchall()
        id_searched = str(id_json[0][0])

        cursor.execute(f"SELECT * FROM SONG WHERE id_artist = '{id_searched}'")
        datas = cursor.fetchall()

        for data in datas:
            id_konten = str(data[0])
            cursor.execute(f"SELECT * FROM KONTEN WHERE id = '{id_konten}'")
            tmp = cursor.fetchall()
            songs.append(tmp)

        for song_group in songs:
            group_list = []
            for song in song_group:
                song_dict = {
                    'id': song[0],
                    'title': song[1],
                    'release_date': song[2],
                    'year': song[3],
                    'duration': song[4]
                }
                group_list.append(song_dict)
            formatted_songs.append(group_list)
        cursor.execute("set search_path to public")

    return formatted_songs


@csrf_exempt
def register(request):
    return render(request, 'register.html')

@csrf_exempt
def register_label(request):
    context = {
        "is_logged_in": False
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        random_id = str(uuid.uuid4())

        with conn.cursor() as cursor:
            cursor.execute('set search_path to marmut')
            cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
            hak_cipta = cursor.fetchall()
            random_hak_cipta = str(random.choice(hak_cipta)[0])
            try: 
                cursor.execute(f"INSERT INTO LABEL(id, nama, email, password, kontak, id_pemilik_hak_cipta) values ('{random_id}', '{nama}', '{email}', '{password}', '{kontak}', '{random_hak_cipta}')")
            except Exception as e:
                msg = str(e).split('\n')[0]
                print(msg)
                return render(request, "register_label.html")

        return redirect('authentication:login')
    
    return render(request, "Register_Label.html", context)

@csrf_exempt
def register_pengguna(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        if(gender) == ('Laki-laki'):
            no_gender = 1
        else:
            no_gender = 0
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        roles = request.POST.getlist('role')
        if len(roles) == 0:
            verified = False
        else:
            verified = True
        with conn.cursor() as cursor:
            try:
                cursor.execute("set search_path to marmut")
                cursor.execute(f"INSERT INTO AKUN(email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) values ('{email}', '{password}', '{nama}', '{no_gender}', '{tempat_lahir}', '{tanggal_lahir}', '{verified}', '{kota_asal}')")
                for i in roles:
                    if i == "Podcaster":
                        cursor.execute(f"INSERT INTO PODCASTER(email) values ('{email}')")
                    elif i == "Artist":
                        cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
                        hak_cipta = cursor.fetchall()
                        random_hak_cipta = str(random.choice(hak_cipta)[0])
                        id_random = str(uuid.uuid4())
                        cursor.execute(f"INSERT INTO ARTIST(id, email_akun, id_pemilik_hak_cipta) values ('{id_random}', '{email}', '{random_hak_cipta}')")
                    elif i == "Songwriter":
                        cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
                        hak_cipta = cursor.fetchall()
                        random_hak_cipta = str(random.choice(hak_cipta)[0])
                        id_random = str(uuid.uuid4())
                        cursor.execute(f"INSERT INTO SONGWRITER(id, email_akun, id_pemilik_hak_cipta) values ('{id_random}', '{email}', '{random_hak_cipta}')")
            except Exception as e:
                msg = str(e).split('\n')[0]
                return render(request, "Register_Pengguna.html")

            context = {
                "is_logged_in": False
            }
            return redirect('authentication:login')

    
    context = {
        "is_logged_in": False
    }
    return render(request, "Register_Pengguna.html", context)
