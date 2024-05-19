from django.urls import path
from kelolapodcast.views import *;

app_name = 'kelolapodcast'

urlpatterns = [
    path('', list_podcast, name='list_podcast'), 
    path('create-podcast', create_podcast, name='create_podcast'), 
    path('delete-podcast/<str:id_podcast>', delete_podcast, name='delete_podcast'),
    path('create-episode/<str:podcast_id>', create_episode, name='create_episode'), 
    path('list-episode/<str:podcast_id>', list_episode, name='list_episode'), 
    path('delete-episode/<str:id_episode>', delete_episode, name='delete_episode'),
]