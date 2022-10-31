# -*- encoding: utf-8 -*-
from django.urls import path, include
from .views import recipe_img

urlpatterns = [
    path("img/<str:recipe_name>", recipe_img, name='recipe_img'),
]
