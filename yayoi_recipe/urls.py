# -*- encoding: utf-8 -*-
from django.urls import path
from .views import recipe_types, delete_recipe_type, list_recipes, upload_recipe, recipe_edit, recipe_pdf, delete_recipe

urlpatterns = [
    path("recipe_type", recipe_types, name='recipe_types'),
    path("recipe_type/<str:recipe_type>/delete", delete_recipe_type, name='delete_recipe_type'),
    path("upload_recipe", upload_recipe, name='upload_recipe'),
    path("<str:recipe_type>", list_recipes, name='list_all_recipes'),
    path("<str:recipe_type>/<str:recipe_name>", recipe_edit, name='recipe_edit'),
    path("<str:recipe_type>/<str:recipe_name>/pdf", recipe_pdf, name='recipe_pdf'),
    path("<str:recipe_type>/<str:recipe_name>/delete", delete_recipe, name='delete_recipe'),
]
