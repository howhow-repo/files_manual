# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from employee.models import Department, BranchLocation

schema_view = get_schema_view(
    openapi.Info(
        title="Yayoi API",
        default_version='v1',
        description="",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


Department.objects.get_or_create(name='其他')
Department.objects.get_or_create(name='內場')
Department.objects.get_or_create(name='外場')
Department.objects.get_or_create(name='管理')
BranchLocation.objects.get_or_create(name='其他')


urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path("", include("apps.authentication.urls")),  # Auth routes - login / register
    path("", include("index.urls")),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api/", include("api.urls")),
    path("user_management/", include("employee.urls")),
    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("demo/", include("apps.demo.urls")),
]
