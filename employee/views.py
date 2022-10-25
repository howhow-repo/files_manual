from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import SignUpForm
from index.forms import UserProfileEdit
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_all_users')

        else:
            msg = 'Form is not valid'
            print(msg)
            print(form.errors.as_data())

    else:
        form = SignUpForm()

    return render(request, "home/create_user.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url="/login/")
def edit_user(request):
    if request.method == "POST":
        pass
    else:
        pass
