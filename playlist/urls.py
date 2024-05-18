from django.urls import path
from . import views

urlpatterns = [
    path('<str:id_user_playlist>/', views.playlist, name='playlist'),
    path('tambahlagu/<str:id_user_playlist>/', views.tambahlagu, name='tambahlagu'),
    path('shuffle/song/', views.shuffle, name='shuffle'),
]