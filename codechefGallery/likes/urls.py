from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('photos/', views.photo, name='index'),
    path('album/', views.albums, name='index')
]
