# -*- encoding: utf-8 -*-
from django.urls import path
from .views import index, update_user_profile


urlpatterns = [
    path("", index, name='index'),
    path("update_user_profile", update_user_profile, name='update_user_profile'),
]
