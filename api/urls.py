# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from api.views import ListUsers,CheckServerHealth


urlpatterns = [
    path('CheckServerHealth', CheckServerHealth.as_view(), name='CheckServerHealth'),
    path('ListUsers', ListUsers.as_view(), name='ListUsers'),
]
