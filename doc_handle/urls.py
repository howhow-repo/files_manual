# -*- encoding: utf-8 -*-
from django.urls import path, include
from .views import recipe_img, recipe_pdf, precaution_doc, precaution_img, stream_video

urlpatterns = [
    path("recipe/img/<str:recipe_name>", recipe_img, name='recipe_img'),
    path("recipe/doc/<str:recipe_name>", recipe_pdf, name='recipe_pdf'),
    path("precaution/img/<str:precaution_name>", precaution_img, name='precaution_img'),
    path("precaution/docs/<str:precaution_name>", precaution_doc, name='precaution_doc'),
]
