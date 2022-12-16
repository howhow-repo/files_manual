from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from lib.fill_form_initial_with_org_data import fill_form_initial_with_org_data
from .forms import UserProfileEdit


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    if request.user.department.name == '管理':
        context['manager'] = True
    form = UserProfileEdit()

    if request.method == 'POST':
        update_form = UserProfileEdit(data=request.POST, instance=request.user)
        if update_form.is_valid():
            user = update_form.save(commit=False)
            user.save()
            context['Msg'] = 'Success'
        else:
            context['errMsg'] = update_form.errors.as_data()

    form = fill_form_initial_with_org_data(request.user, form)

    context['form'] = form
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
