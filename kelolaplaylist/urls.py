from django.urls import path
from . import views

urlpatterns = [
    path('', views.kelolaplaylist, name='kelolaplaylist'),
    path('edit/<str:id_playlist>', views.editplaylist, name='editplaylist'),
    path('delete/<str:id_playlist>', views.deleteplaylist, name='deleteplaylist'),
]