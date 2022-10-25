from django.contrib.auth.decorators import login_required
from django.template import loader
from decouple import config
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileEdit


CONTEXT = {
    "PROJECT_TITLE": config('PROJECT_TITLE', default='unnamed'),
    "segment": 'Index',
}


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    User = get_user_model()
    user = User.objects.get(username=request.user)
    form = UserProfileEdit()

    if request.method == 'POST':
        update_form = UserProfileEdit(data=request.POST, instance=request.user)
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
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


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

    html_template = loader.get_template('home/change_password.html')
    return HttpResponse(html_template.render({'form': form}, request))
