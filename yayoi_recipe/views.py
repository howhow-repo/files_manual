# -*- encoding: utf-8 -*-
from datetime import datetime

from django.db.models import ProtectedError

from .models import RecipeType, Recipe
from employee.views import manager_required
from .forms import RecipeTypeForm, DeleteRecipeTypeForm, RecipeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def handle_uploaded_file(f, path:str, filename: str):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def recipe_types(request):
    context = {'segment': 'recipe_types', 'manager': True}
    if request.method == "POST":
        form = RecipeTypeForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context['errMsg'] = 'Error validating the form'
    else:
        form = RecipeTypeForm()
    context['types'] = RecipeType.objects.all()
    context['form'] = form
    html_template = loader.get_template('home/recipe_types.html')
    return HttpResponse(html_template.render(context, request))


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_recipe_type(request, recipe_type):
    context = {'manager': True, 'segment': 'recipe_type', 'delete_recipe_type': recipe_type, 'form': DeleteRecipeTypeForm()}
    if request.method == "POST":
        form = DeleteRecipeTypeForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            recipe_type = RecipeType.objects.get(name=recipe_type)
            try:
                recipe_type.delete()
                return HttpResponseRedirect('/recipes/recipe_type')
            except ProtectedError:
                context.update({'errMsg': '分類使用中，無法刪除。'})
    else:
        form = DeleteRecipeTypeForm()
    context['form'] = form
    html_template = loader.get_template('home/delete_recipe_type.html')
    return HttpResponse(html_template.render(context, request))


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
    html_template = loader.get_template('home/upload_recipe.html')
    return HttpResponse(html_template.render(context, request))


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
def add_recipe(request):
    pass
