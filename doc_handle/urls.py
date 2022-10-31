# -*- encoding: utf-8 -*-
from django.urls import path, include
from .views import recipe_img, recipe_pdf

urlpatterns = [
    path("img/<str:recipe_name>", recipe_img, name='recipe_img'),
    path("doc/<str:recipe_name>", recipe_pdf, name='recipe_pdf'),
]
