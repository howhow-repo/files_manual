# -*- encoding: utf-8 -*-
from django.urls import path
from .views import upload_precaution_type

urlpatterns = [
    path("precaution_types", upload_precaution_type, name='precaution_types'),
]
