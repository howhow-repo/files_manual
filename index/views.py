from django.contrib.auth.decorators import login_required
from django.template import loader
from decouple import config
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django import forms
from .forms import UserProfileEdit


CONTEXT = {
    "PROJECT_TITLE": config('PROJECT_TITLE', default='unnamed'),
    "segment": 'Index',
}


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    if request.GET.get('errMsg'):
        context['errMsg'] = request.GET.get('errMsg')

    # User data
    User = get_user_model()
    user = User.objects.get(username=request.user)

    # form for update
    p = UserProfileEdit()
    for element in p.fields:
        data_from_user = getattr(user, element)
        p.fields[element].widget.attrs.update({'class': 'form-control'})
        if data_from_user is None or data_from_user == "":
            p.fields[element].widget.attrs.update({'class': 'form-control'})
        else:
            p.fields[element].initial = data_from_user

    context['form'] = p
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def update_user_profile(request):
    update_form = UserProfileEdit(data=request.POST, instance=request.user)
    if update_form.is_valid():
        user = update_form.save(commit=False)
        user.save()
        return HttpResponseRedirect('/')
    else:
        errMsg = update_form.errors.as_data()
        return HttpResponseRedirect(f'/?errMsg={errMsg}')



