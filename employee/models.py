# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


DEPARTMENT_CHOICES = (
    ('內場', '內場'),
    ('外場', '外場'),
    ('管理', '管理'),
    ('開發', '開發'),
    ('其他', '其他')
)


class User(AbstractUser):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default='其他')
    is_accept = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, null=True)
