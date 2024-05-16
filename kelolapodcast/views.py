from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import json
from django.http import JsonResponse

def create_podcast(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'create_podcast.html', context)

def list_podcast(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'list_podcast.html', context)

def create_episode(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'create_episode.html', context)

def list_episode(request):
    context = {
        'variable': 'nilai_variable'
    }
    return render(request, 'list_episode.html', context)