from django.urls import path
from melihatchart.views import *;

app_name = 'melihatchart'

urlpatterns = [
    path('', chart_list, name='chart_list'), 
    path('chart-detail/<str:id>/<str:tipe>', chart_detail, name='chart_detail'),
]