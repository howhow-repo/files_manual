# -*- encoding: utf-8 -*-
import os
import re
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse
from wsgiref.util import FileWrapper
from .lib import RangeFileWrapper
from django.template import loader
from yayoi_recipe.models import Recipe
from precautions.models import Precaution
from django.contrib.auth.decorators import login_required
from django.conf import settings

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
video_extension = ['mp4', 'mov']
doc_extension = ['pdf']


@login_required(login_url="/login/")
def recipe_img(request, recipe_name):
    try:
        recipe = Recipe.objects.get(name=recipe_name)
        path = recipe.picture.name
    except Exception:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))

    if os.path.isfile(path):
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


def stream_video(request, path):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length),
                                     status=206, content_type='video/mp4')
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)

    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type='video/mp4')
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    resp['Content-Disposition'] = 'inline'
    return resp


@login_required(login_url="/login/")
def precaution_img(request, precaution_name):
    try:
        precaution_doc = Precaution.objects.get(name=precaution_name)
        path = precaution_doc.cover.name
    except Exception:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponseNotFound(HttpResponse(html_template.render({}, request)))

    if os.path.isfile(path):
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    else:
        with open(settings.STATICFILES_DIRS[0] + '/assets/images/default_precaution_img.png', "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")


@login_required(login_url="/login/")
def precaution_doc(request, precaution_name):
    precaution_doc = Precaution.objects.get(name=precaution_name)
    path = precaution_doc.file.name
    file_extension = path.split('.')[-1]
    if file_extension in video_extension:
        return stream_video(request, path)
    elif file_extension in doc_extension:
        pass  # TODO


