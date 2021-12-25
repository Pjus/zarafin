from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView
from . import views

app_name = "search"

urlpatterns = [
    path('search/', views.search, name='search'),
]
