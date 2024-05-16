from django.urls import path
from . import views

urlpatterns = [
    path('', views.song_detail, name='song_detail'),
]