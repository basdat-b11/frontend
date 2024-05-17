from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', show_landingpage, name='landing-page'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name="logout"),
    path('register/label/', register_label, name='register-label'),
    path('register/pengguna/', register_pengguna, name='register-pengguna'),
    path('dashboard/', dashboard, name='dashboard')
]