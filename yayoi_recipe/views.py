# -*- encoding: utf-8 -*-
import os
from datetime import datetime
from django.db.models import ProtectedError
from django.shortcuts import render

from .models import RecipeType, Recipe
from employee.views import manager_required, set_org_data_in_form_initial
from .forms import RecipeTypeForm, RecipeForm, DeleteRecipeTypeForm, DeleteRecipeForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def remove_document(path):
    if os.path.isfile(path):
        os.remove(path)


def delete_recipe_related_file(recipe_instance):
    img_path = recipe_instance.cover.name
    pdf_path = recipe_instance.pdf.name
    if os.path.isfile(img_path):
        os.remove(img_path)
    if os.path.isfile(pdf_path):
        os.remove(pdf_path)


def http_not_found_page(request):
    html_template = loader.get_template('home/page-404.html')
    return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def recipe_types(request):
    context = {'segment': 'recipe_types'}
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
    recipe_type = RecipeType.objects.filter(name=recipe_type).first()
    if not recipe_type:
        return http_not_found_page(request)

    context = {'segment': 'recipe_type', 'delete_recipe_type': recipe_type}
    if request.method == "POST":
        form = DeleteRecipeTypeForm(request.POST)
        if form.is_valid():
            try:
                recipe_type.delete()
                return HttpResponseRedirect('/recipes/recipe_type')
            except ProtectedError:
                context.update({'errMsg': '?????????????????????????????????'})
    else:
        form = DeleteRecipeTypeForm()
    context['form'] = form
    return render(request, 'delete_recipe_type.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def upload_recipe(request):
    context = {'segment': 'upload_recipe'}
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
def list_recipe_types(request):
    context = {'segment': 'recipes', 'types': RecipeType.objects.all()}
    return render(request, 'search_by_types.html', context)


@require_http_methods(["GET"])
@login_required(login_url="/login/")
def list_recipes(request, recipe_type: str = 'all'):
    context = {'segment': 'recipes'}
    if recipe_type == 'all':
        context['recipes'] = Recipe.objects.all()
    else:
        recipe_type = RecipeType.objects.filter(name=recipe_type).first()
        if not recipe_type:
            return http_not_found_page(request)
        context['recipes'] = Recipe.objects.filter(type__name=recipe_type)

    if not (context['recipes']):
        context['empty'] = True
    return render(request, 'list_recipes.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def update_recipe(request, recipe_type: str, recipe_name: str):
    context = {'segment': 'recipes', 'recipe_name': recipe_name, 'recipe_type': recipe_type}

    recipe_instance = Recipe.objects.filter(name=recipe_name).first()
    if not recipe_instance or recipe_instance.type.name != recipe_type:
        return http_not_found_page(request)
    old_pdf_path = recipe_instance.pdf.name
    old_img_path = recipe_instance.cover.name

    if request.method == "POST":
        recipe_instance.last_update = datetime.now()
        form = RecipeForm(request.POST, request.FILES, instance=recipe_instance)
        if form.is_valid():
            if 'cover' in form.changed_data:
                remove_document(old_img_path)

            if 'pdf' in form.changed_data:
                remove_document(old_pdf_path)

            form.save()
            return HttpResponseRedirect('/recipes/all')
    else:
        form = RecipeForm()

    form = set_org_data_in_form_initial(recipe_instance, form, ['cover', 'pdf'])
    form.fields['pdf'].required = False
    context['form'] = form
    return render(request, 'edit_recipe.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_recipe(request, recipe_type: str, recipe_name: str):
    recipe_instance = Recipe.objects.filter(name=recipe_name).first()
    if not recipe_instance or recipe_instance.type.name != recipe_type:
        return http_not_found_page(request)

    context = {'segment': 'recipes', 'recipe_type': recipe_type, 'delete_recipe': recipe_name}
    if request.method == "POST":
        form = DeleteRecipeForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            delete_recipe_related_file(recipe_instance)
            recipe_instance.delete()
            return HttpResponseRedirect('/recipes/all')
    else:
        form = DeleteRecipeForm()
    context['form'] = form
    return render(request, 'delete_recipe.html', context)
