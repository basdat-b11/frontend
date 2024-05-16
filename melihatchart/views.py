from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import json
from django.http import JsonResponse

def daily_chart_detail(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'daily_chart_detail.html', context)

def weekly_chart_detail(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'weekly_chart_detail.html', context)

def monthly_chart_detail(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'monthly_chart_detail.html', context)

def yearly_chart_detail(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'yearly_chart_detail.html', context)

def chart_list(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'chart_list.html', context)