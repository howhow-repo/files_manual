# -*- encoding: utf-8 -*-
from django.urls import path
from .views import recipe_types, delete_recipe_type, list_recipes, upload_recipe, update_recipe, delete_recipe

urlpatterns = [
    path("recipe_type", recipe_types, name='recipe_types'),
    path("recipe_type/<str:recipe_type>/delete", delete_recipe_type, name='delete_recipe_type'),
    path("upload_recipe", upload_recipe, name='upload_recipe'),
    path("<str:recipe_type>", list_recipes, name='list_all_recipes'),
    path("<str:recipe_type>/<str:recipe_name>", update_recipe, name='update_recipe'),
    path("<str:recipe_type>/<str:recipe_name>/delete", delete_recipe, name='delete_recipe'),
]
