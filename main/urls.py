from django.urls import include,path
from django.urls import path
from main.views import subscription_page, bayar_paket, riwayat_langganan, unduhan_lagu, pencarian
from kelolaalbum.views import *

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('langganan-paket/', subscription_page, name='susbcription_page'),
    path('pembayaran-paket/', bayar_paket, name='bayar_paket'),
    path('riwayat-langganan/', riwayat_langganan, name='riwayat_langganan'),
    path('unduhan-lagu/', unduhan_lagu, name='unduhan_lagu'),
    path('cari', pencarian, name='pencarian'),
]