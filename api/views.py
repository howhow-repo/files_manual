from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from django.contrib.auth import get_user_model


class ListUsers(APIView):
    """
        test
    """

    @swagger_auto_schema(
        operation_summary='check swagger format.'
    )
    def get(self, request):
        User = get_user_model()
        users = User.objects.values()
        for u in users:
            print(u)

        return JsonResponse({},safe=False)
