from django.urls import path
from main.views import *;

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('', first_view, name='first_view'),
    path('test', test_akun, name='test_akun'),
    path('role-register-view/', role_register_view, name='role-register-view'),
    path('register-pengguna/', register_pengguna, name='register-pengguna'),
    #path('register-pengguna/', register_pengguna, name='register-pengguna'),
    path('login/', login_user, name='login'),
]