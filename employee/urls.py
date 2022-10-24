from django.urls import path
from .views import view_all_users



urlpatterns = [
    path("", view_all_users, name='view_all_users'),

]