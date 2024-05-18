from django.urls import path
from melihatchart.views import *;

app_name = 'melihatchart'

urlpatterns = [
    path('', chart_list, name='chart_list'), 
    path('daily-chart-detail', daily_chart_detail, name='daily_chart_detail'), 
    path('weekly-chart-detail', weekly_chart_detail, name='weekly_chart_detail'), 
    path('monthly-chart-detail', monthly_chart_detail, name='monthly_chart_detail'), 
    path('yearly-chart-detail', yearly_chart_detail, name='yearly_chart_detail'), 
]