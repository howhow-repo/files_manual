from django.urls import path
from .views import view_all_users,register_user



urlpatterns = [
    path("", view_all_users, name='view_all_users'),
    path("register_user", register_user, name='register_user'),
]
