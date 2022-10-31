# -*- encoding: utf-8 -*-
from datetime import datetime

from django.db.models import ProtectedError
from django.shortcuts import render

from .models import RecipeType, Recipe
from employee.views import manager_required
from .forms import RecipeTypeForm, RecipeForm, DeleteRecipeTypeForm, DeleteRecipeForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def is_manager(request):
    User = get_user_model()
    user = User.objects.get(username=request.user)
    if user.department.name == '管理':
        return True
    else:
        return False


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def recipe_types(request):
    context = {'segment': 'recipe_types', 'manager': True}
    if request.method == "POST":
        form = RecipeTypeForm(request.POST)
        if form.is_valid():
            form.save()
            form = RecipeTypeForm()
        else:
            context['errMsg'] = 'Error validating the form'
    else:
        form = RecipeTypeForm()
    context['types'] = RecipeType.objects.all()
    context['form'] = form
    return render(request, 'recipe_types.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_recipe_type(request, recipe_type):
    context = {'manager': True, 'segment': 'recipe_type', 'delete_recipe_type': recipe_type, 'form': DeleteRecipeTypeForm()}
    if request.method == "POST":
        form = DeleteRecipeTypeForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            recipe_type = RecipeType.objects.filter(name=recipe_type)
            try:
                recipe_type.delete()
                return HttpResponseRedirect('/recipes/recipe_type')
            except ProtectedError:
                context.update({'errMsg': '分類使用中，無法刪除。'})
    else:
        form = DeleteRecipeTypeForm()
    context['form'] = form
    return render(request, 'delete_recipe_type.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def upload_recipe(request):
    context = {'segment': 'upload_recipe', 'manager': True}
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context['Msg'] = f'Success'
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = RecipeForm()
    context['form'] = form
    return render(request, 'upload_recipe.html', context)


@require_http_methods(["GET"])
@login_required(login_url="/login/")
def list_recipes(request, recipe_type: str = 'all'):
    context = {'segment': 'recipes'}
    if is_manager(request):
        context['manager'] = True
    if recipe_type == 'all':
        recipes = Recipe.objects.all()
    else:
        try:
            recipetype = RecipeType.objects.get(name=recipe_type)
            recipes = Recipe.objects.get(type=recipetype)
        except Exception:
            html_template = loader.get_template('home/page-404.html')
            return HttpResponseNotFound(HttpResponse(html_template.render(context, request)))
    for r in recipes:
        context['recipes'] = recipes

    return render(request, 'list_recipes.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def recipe_edit(request, recipe_type: str, recipe_name: str):
    context = {'segment': 'recipes', 'manager': True}
    form = RecipeForm()
    try:
        recipetype = RecipeType.objects.get(name=recipe_type)
        recipe_instence = Recipe.objects.get(name=recipe_name)
    except Exception:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render(context, request)))
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe_instence)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recipes/all')

    for element in form.fields:
        initial_data = getattr(recipe_instence, element)
        if initial_data is not None or initial_data != "":
            form.fields[element].initial = initial_data

    context['form'] = form
    context['recipe_name'] = recipe_name
    context['recipe_type'] = recipe_type
    return render(request, 'edit_recipe.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_recipe(request, recipe_type: str, recipe_name: str):
    context = {'segment': 'recipes', 'manager': True, 'recipe_type': recipe_type,'delete_recipe': recipe_name}
    try:
        recipetype = RecipeType.objects.get(name=recipe_type)
        recipe_instence = Recipe.objects.get(name=recipe_name)
    except Exception:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render(context, request)))

    if request.method == "POST":
        form = DeleteRecipeForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            recipe_instence.delete()
            return HttpResponseRedirect('/recipes/all')
    else:
        form = DeleteRecipeForm()
    context['form'] = form
    return render(request, 'delete_recipe.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def recipe_pdf(request, recipe_type: str, recipe_name: str):
    pass



