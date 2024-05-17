from django.urls import include,path
from main.views import test_akun

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('', test_akun, name='test_akun'), 
    path('kelolaplaylist/', include('kelolaplaylist.urls')),
    path('songdetail/', include('songdetail.urls')),
    path('playlist/', include('playlist.urls')),
]