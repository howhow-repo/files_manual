# -*- encoding: utf-8 -*-
from django.urls import path
from .views import upload_precaution_type, delete_precaution_type, upload_precaution

urlpatterns = [
    path("precaution_types", upload_precaution_type, name='precaution_types'),
    path("precaution_types/<str:precaution_type>/delete", delete_precaution_type, name='delete_precaution_type'),
    path("upload_precaution", upload_precaution, name='upload_precaution'),
]
