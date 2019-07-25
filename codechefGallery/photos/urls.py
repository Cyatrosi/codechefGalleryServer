from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('my/', views.my,name='index'),
    path('album/<str:albumId>/', views.albumPics,name='index'),
    path('<str:userId>/', views.photo,name='photo'),
]