# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include
from api.views import ListUsers


urlpatterns = [
    path('ListUsers/', ListUsers.as_view(), name='ListUsers'),
]
