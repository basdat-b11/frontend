from django.urls import path
from playpodcast.views import *;

app_name = 'playpodcast'

urlpatterns = [
    path('/podcast-detail/<str:podcast_id>', podcast_detail, name='podcast_detail'), 
]