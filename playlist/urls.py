from django.urls import path
from . import views

urlpatterns = [
    path('<str:id_playlist>/', views.playlist, name='playlist'),
    path('tambahlagu/<str:id_playlist>/', views.tambahlagu, name='tambahlagu'),
]