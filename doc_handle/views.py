# -*- encoding: utf-8 -*-
import logging
import os
from django.http import HttpResponse, HttpResponseNotFound
from .lib import stream_video
from django.template import loader
from yayoi_recipe.models import Recipe
from precautions.models import Precaution
from django.contrib.auth.decorators import login_required
from django.conf import settings

logger = logging.getLogger(__name__)

video_extension = ['mp4', 'mov']
doc_extension = ['pdf']


@login_required(login_url="/login/")
def recipe_img(request, recipe_name):
    try:
        recipe = Recipe.objects.get(name=recipe_name)
        path = recipe.cover.name
    except Exception:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))

    if path and os.path.isfile(path):
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    else:
        with open(settings.STATICFILES_DIRS[0] + '/assets/images/default_recipe_img.png', "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")


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


@login_required(login_url="/login/")
def precaution_img(request, precaution_name):
    try:
        precaution_doc = Precaution.objects.get(name=precaution_name)
        path = precaution_doc.cover.name
    except Exception:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))

    if path and os.path.isfile(path):
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    else:
        with open(settings.STATICFILES_DIRS[0] + '/assets/images/default_precaution_img.png', "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")


@login_required(login_url="/login/")
def precaution_doc(request, precaution_name):
    doc = Precaution.objects.get(name=precaution_name)
    path = doc.file.name
    file_extension = str.lower(path.split('.')[-1])
    if file_extension in video_extension:
        return stream_video(request, path)
    elif file_extension in doc_extension:
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="application/pdf")
    else:
        logger.warning(f"precaution_doc {path} not in file_extension.")
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))


