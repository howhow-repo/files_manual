# -*- encoding: utf-8 -*-
from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


class ListUsers(APIView):
    """
        test
    """

    @swagger_auto_schema(
        operation_summary='check swagger format.'
    )
    def get(self, request):
        User = get_user_model()
        users = User.objects.all()
        for u in users:
            print(u.username, u.department, u.is_accept)

        return JsonResponse({}, safe=False)


class CheckServerHealth(APIView):
    """
        For checking server is alive.
    """

    @swagger_auto_schema(
        operation_summary='Use it as ping.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'I_AM': openapi.Schema(type=openapi.TYPE_STRING, description='Please enter who you are.'),
            }
        )
    )
    def post(self, request):
        print(request.GET)
        print(request.data)
        if request.data.get('I_AM') and str.lower(request.data.get('I_AM')) == 'app':
            healthy_msg = {
                'msg': 'I am alive!',
                'errCode': 0
            }
            return JsonResponse(healthy_msg)
        return HttpResponseForbidden()
