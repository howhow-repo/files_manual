# -*- encoding: utf-8 -*-
from django.urls import path
from .views import show_recipe_types, show_recipes, show_recipe_info

urlpatterns = [
    path("", show_recipe_types, name='show_recipe_types'),
    path("<str:recipe_type>", show_recipes, name='show_recipes'),
    path("<str:recipe_type>/<int:recipe_id>", show_recipe_info, name='show_recipe_info'),
]
