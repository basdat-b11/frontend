from django.urls import path
from . import views

urlpatterns = [
    path('', views.song_detail, name='song_detail'),
    path('view/<str:id_konten>/', views.song_detail_by_id, name='song_detail'),
    path('play/', views.play, name='play'),
    path('play2/<str:id_konten>', views.play2, name='play2'),
    path('download/', views.download, name='download'),
    path('delete/<str:id_playlist>/<str:id_konten>/', views.delete, name='delete'),
    path('redirect-choice/', views.redirectchoice, name='redirectchoice'),
    path('redirect-download/', views.redirectdownload, name='redirectdownload'),
]