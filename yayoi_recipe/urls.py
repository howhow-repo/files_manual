# -*- encoding: utf-8 -*-
from django.urls import path
from .views import recipe_types, delete_recipe_type, show_recipes, show_recipe_info, upload_recipe

urlpatterns = [
    path("recipe_type", recipe_types, name='recipe_types'),
    path("recipe_type/<str:recipe_type>/delete", delete_recipe_type, name='delete_recipe_type'),
    path("upload_recipe", upload_recipe, name='upload_recipe'),
    path("<str:recipe_type>", show_recipes, name='show_recipes'),
    path("<str:recipe_type>/<int:recipe_name>", show_recipe_info, name='show_recipe_info'),
]
