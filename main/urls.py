from django.urls import include,path
from django.urls import path
from main.views import subscription_page, bayar_paket, riwayat_langganan, unduhan_lagu, pencarian
from kelolaalbum.views import *

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('kelolaalbum/', include('kelolaalbum.urls')),
    path('kelolaplaylist/', include('kelolaplaylist.urls')),
    path('songdetail/', include('songdetail.urls')),
    path('playlist/', include('playlist.urls')),
    # path('create-album', create_album, name='create_album'), 
    # path('list-album', list_album, name='list_album'),
    # path('list-album-label', list_album_label, name='list_album_label'),
    # path('create-lagu', create_lagu, name='create_lagu'),
    # path('cek-royalti', cek_royalti, name='cek_royalti'),
    # path('lagulist-album', lagulist_album, name='lagulist_album'),
    # path('    lagulist-album-label', lagulist_album_label, name='lagulist_album_label'),
    path('langganan-paket/', subscription_page, name='susbcription_page'),
    path('pembayaran-paket/', bayar_paket, name='bayar_paket'),
    path('riwayat-langganan/', riwayat_langganan, name='riwayat_langganan'),
    path('unduhan-lagu/', unduhan_lagu, name='unduhan_lagu'),
    path('cari', pencarian, name='pencarian'),
    # path('lagulist-album-label', lagulist_album_label, name='lagulist_album_label'),
]