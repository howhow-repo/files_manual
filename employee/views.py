from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


def view_all_users(request):
    context = {
        'segment': 'user_management',
        'users': []
    }
    User = get_user_model()
    users = User.objects.all()
    for u in users:
        if u.department != '開發':
            context['users'].append({
                'username': u.username,
                'nickname': u.nickname,
                'location': u.location,
                'department': u.department,
                'is_accept': u.is_accept,
                'phone_number': u.phone_number,
            })
    html_template = loader.get_template('home/user_management.html')
    return HttpResponse(html_template.render(context, request))

