from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import SignUpForm, DeleteUserForm
from index.forms import UserProfileEdit
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


def is_manager(request):
    User = get_user_model()
    user = User.objects.get(username=request.user)
    if user.department.name == '管理':
        return True
    else:
        return False


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def view_all_users(request):
    if not is_manager(request):
        html_template = loader.get_template('home/page-403.html')
        return HttpResponse(html_template.render({}, request))

    context = {
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
                'is_accept': u.is_accept,
                'phone_number': u.phone_number,
            })
    html_template = loader.get_template('home/user_management.html')
    return HttpResponse(html_template.render(context, request))


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def register_user(request):
    if not is_manager(request):
        html_template = loader.get_template('home/page-403.html')
        return HttpResponse(html_template.render({}, request))
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

    return render(request, "home/create_user.html",
                  {
                      'segment': 'user_management',
                      "form": form,
                      "msg": msg,
                      "success": success
                  })


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def edit_user(request, username):
    if not is_manager(request):
        html_template = loader.get_template('home/page-403.html')
        return HttpResponse(html_template.render({}, request))
    context = {'segment': 'user_management', 'edit_user': username}
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
            context['errMsg'] = update_form.errors.as_data()

    for element in form.fields:
        data_from_user = getattr(user, element)
        form.fields[element].widget.attrs.update({'class': 'form-control'})
        if data_from_user is None or data_from_user == "":
            form.fields[element].widget.attrs.update({'class': 'form-control'})
        else:
            form.fields[element].initial = data_from_user

    context['form'] = form
    html_template = loader.get_template('home/edit_user.html')
    return HttpResponse(html_template.render(context, request))


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_user(request, username):
    if not is_manager(request):
        html_template = loader.get_template('home/page-403.html')
        return HttpResponse(html_template.render({}, request))
    User = get_user_model()
    user = User.objects.get(username=username)

    if request.method == "POST":  # 接受post update
        form = DeleteUserForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            user.delete()
            messages.success(request, "The user is deleted")
        return HttpResponseRedirect("/user_management")

    else:
        context = {'segment': 'user_management', 'delete_user': username, 'form': DeleteUserForm()}
        html_template = loader.get_template('home/delete_user_confirm.html')
        return HttpResponse(html_template.render(context, request))

