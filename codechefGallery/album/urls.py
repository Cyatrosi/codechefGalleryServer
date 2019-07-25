from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('my/', views.my,name='index'),
    path('<str:userId>/', views.albums,name='photo'),
]