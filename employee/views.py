from django.shortcuts import render
from django.contrib.auth import get_user_model


def view_all_users(request):
    context = {
        'segment': 'user_management',
        'users': []
    }
    User = get_user_model()
    users = User.objects.all()
    for u in users:
        context['users'].append({
            'username': u.username,
            'nickname': u.nickname,
            'location': u.location,
            'department': u.department,
            'is_accept': u.is_accept,
            'phone_number': u.phone_number,
        })

