# -*- encoding: utf-8 -*-
from django.urls import path
from .views import upload_precaution_type, delete_precaution_type
from .views import upload_precaution, list_precautions, percaution_detail, update_percaution

urlpatterns = [
    path("precaution_types", upload_precaution_type, name='precaution_types'),
    path("precaution_types/<str:precaution_type>/delete", delete_precaution_type, name='delete_precaution_type'),
    path("upload_precaution", upload_precaution, name='upload_precaution'),
    path("<str:precaution_type>", list_precautions, name='list_precautions'),
    path("<str:precaution_type>/<str:precaution_name>", percaution_detail, name='percaution_detail'),
    path("<str:precaution_type>/<str:precaution_name>/update", update_percaution, name='update_precaution'),
    path("<str:precaution_type>/<str:precaution_name>/delete", list_precautions, name='delete_precaution'),
]
