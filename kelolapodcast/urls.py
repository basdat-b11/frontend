from django.urls import path
from kelolapodcast.views import *;

app_name = 'kelolapodcast'

urlpatterns = [
    path('', list_podcast, name='list_podcast'), 
    path('create-podcast', create_podcast, name='create_podcast'), 
    path('create-episode/<str:id_podcast>', create_episode, name='create_episode'), 
    path('list-episode/<str:id_podcast>', list_episode, name='list_episode'), 
]