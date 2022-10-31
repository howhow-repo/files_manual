# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound
from PIL import Image
from django.shortcuts import render
from django.template import loader

from yayoi_recipe.models import Recipe
from django.contrib.auth.decorators import login_required
from django.conf import settings


def try_to_open_as_image(filename):
    file_extension = ['jpeg', 'jpg', 'png', 'bmp']
    for ex in file_extension:
        try:
            with open(filename+'.' + ex, "rb") as file:
                return HttpResponse(file.read(), content_type="image/jpeg")
        except Exception:
            continue
    raise FileNotFoundError(f'did not find img {filename}')


@login_required(login_url="/login/")
def recipe_img(request, recipe_name):
    try:
        recipe = Recipe.objects.get(name=recipe_name)
        path = recipe.picture.name
    except Exception:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))

    try:
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        return HttpResponse(red, content_type="image/jpeg")


@login_required(login_url="/login/")
def recipe_pdf(request, recipe_name):
    try:
        recipe = Recipe.objects.get(name=recipe_name)
        path = recipe.pdf.name
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="application/pdf")
    except IOError:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))
