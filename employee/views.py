from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import SignUpForm, DeleteUserForm
from index.forms import UserProfileEdit
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader


def manager_required(func):  # use as decorator
    def wrapper(request, *args, **kwargs):
        User = get_user_model()
        user = User.objects.get(username=request.user)
        if user.department.name == '管理':
            return func(request, *args, **kwargs)
        else:
            html_template = loader.get_template('home/page-403.html')
            return HttpResponseForbidden(HttpResponse(html_template.render({}, request)))
    return wrapper


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def view_all_users(request):
    context = {
        'manager': True,
        'segment': 'user_management',
        'users': []
    }
    User = get_user_model()
    users = User.objects.all()
    for u in users:
        if u.username != request.user.username:
            context['users'].append({
                'username': u.username,
                'nickname': u.nickname,
                'location': u.location,
                'department': u.department,
                'phone_number': u.phone_number,
            })
    return render(request, 'user_management.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
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
    else:
        form = SignUpForm()
    return render(request, "create_user.html",
                  {
                      'manager': True,
                      'segment': 'user_management',
                      'form': form,
                      'msg': msg,
                      'success': success
                  })


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def edit_user(request, username):
    context = {'manager': True, 'segment': 'user_management', 'edit_user': username}
    User = get_user_model()
    user = User.objects.get(username=username)
    form = UserProfileEdit()

    if request.method == "POST":  # 接受post update
        update_form = UserProfileEdit(data=request.POST, instance=user)
        if update_form.is_valid():
            user = update_form.save(commit=False)
            user.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = 'Form is not valid'

    for element in form.fields:
        data_from_user = getattr(user, element)
        form.fields[element].widget.attrs.update({'class': 'form-control'})
        if data_from_user is None or data_from_user == "":
            form.fields[element].widget.attrs.update({'class': 'form-control'})
        else:
            form.fields[element].initial = data_from_user

    context['form'] = form
    return render(request, 'edit_user.html', context)



@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_user(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)

    if request.method == "POST":  # 接受post update
        form = DeleteUserForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            user.delete()
            messages.success(request, "The user is deleted")
        return HttpResponseRedirect("/user_management")

    else:
        context = {'manager': True, 'segment': 'user_management', 'delete_user': username, 'form': DeleteUserForm()}
        return render(request, 'delete_user_confirm.html', context)
