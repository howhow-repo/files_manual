# -*- encoding: utf-8 -*-
from .models import RecipeType, Recipe
from employee.views import manager_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def show_recipe_types(request):
    pass


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def show_recipes(request, recipe_type):
    pass


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def show_recipe_info(request):
    pass


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def add_recipe_type(request):
    pass


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def add_recipe(request):
    pass
