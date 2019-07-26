from django.shortcuts import render
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse


def index(request):
    return render(request, 'index.html')
