from django.shortcuts import redirect, render
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages  
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def first_view(request):
    # Lakukan operasi atau logika yang diperlukan
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'LoginRegister.html', context)

def role_register_view(request):
    # Lakukan operasi atau logika yang diperlukan
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'RoleRegister.html', context)

def test_akun(request):
    result = ""
    with connection.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("SELECT * FROM akun;")
        result = cursor.fetchall()
    
    print(result)
    return HttpResponse(result, content_type='application/json', status=200)

def register_pengguna(request):
    
    is_verified = "f"
    is_male = "0"
    if request.method == "POST":
        email = request.POST['inputEmail']
        password = request.POST['inputPasswordl']
        name = request.POST['inputName']
        gender = request.POST['inputGender']
        birth_place = request.POST['inputPlaceOfBirth']
        birth_date = request.POST['inputDateOfBirth']
        city = request.POST['inputCity']
        role = request.POST['inputRole']
        if (role != ""):
            is_verified = "t"

        if (gender == "Male"):
            is_male = "1"

        with connection.cursor() as cursor:
            cursor.execute("Set search_path to marmut;")
            cursor.execute("""
                            INSERT INTO akun (
                                email,
                                password,
                                nama,
                                gender, 
                                tempat_lahir,
                                tanggal_lahir,
                                is_verified,
                                kota_asal
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """, [email, password, name, is_male, birth_place, birth_date, is_verified, city])
    return render(request, 'RegisterPengguna.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        birth_place = request.POST.get('birth_place')
        birth_date = request.POST.get('birth_date')
        city = request.POST.get('city')
        role = request.POST.get('role')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:show_main')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'LoginPage.html', context)

def logout_user(request):
    logout(request)
    return redirect('main:login')