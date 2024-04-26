from django.urls import path
from main.views import test_akun

app_name = 'main'

#testing testing blom paham lanjutnya gmn wkwk
urlpatterns = [
    path('', test_akun, name='test_akun'), 
]