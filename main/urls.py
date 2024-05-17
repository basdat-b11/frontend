from django.urls import include,path
from main.views import test_akun
from django.urls import path
from main.views import *;

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
<<<<<<< HEAD
    path('', first_view, name='first_view'),
    path('test', test_akun, name='test_akun'),
    path('role-register-view/', role_register_view, name='role-register-view'),
    path('register-pengguna/', register_pengguna, name='register-pengguna'),
    #path('register-pengguna/', register_pengguna, name='register-pengguna'),
    path('login/', login_user, name='login'),
=======
    path('', test_akun, name='test_akun'),
    path('kelolaalbum/', include('kelolaalbum.urls')),
    path('kelolaplaylist/', include('kelolaplaylist.urls')),
    path('songdetail/', include('songdetail.urls')),
    path('playlist/', include('playlist.urls')),
    path('create-album', create_album, name='create_album'), 
    path('list-album', list_album, name='list_album'),
    path('list-album-label', list_album_label, name='list_album_label'),
    path('create-lagu', create_lagu, name='create_lagu'),
    path('cek-royalti', cek_royalti, name='cek_royalti'),
    path('lagulist-album', lagulist_album, name='lagulist_album'),
    path('lagulist-album-label', lagulist_album_label, name='lagulist_album_label'),
    path('test', test_akun, name='test_akun')
>>>>>>> bdc8c87a0488f7c070a2d7c2e4121a5e08182fb4
]