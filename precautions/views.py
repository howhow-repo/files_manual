from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from employee.views import manager_required
from yayoi_recipe.views import http_not_found_page
from .forms import PrecautionTypeForm, DeletePrecautionTypeForm, PrecautionForm
from .models import PrecautionType, Precaution


def is_in_database(precaution_type: str = None, precaution_name: str = None):
    if precaution_type and precaution_name != 'all':
        if not PrecautionType.objects.filter(name=precaution_type).exists():
            return False
    if precaution_name:
        if not Precaution.objects.filter(name=precaution_name).exists():
            return False
    return True


def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def upload_precaution_type(request):
    context = {'segment': 'precaution_types', 'manager': True}
    if request.method == "POST":
        form = PrecautionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            form = PrecautionTypeForm()
        else:
            context['errMsg'] = 'Error validating the form'
    else:
        form = PrecautionTypeForm()
    context['types'] = PrecautionType.objects.all()
    context['form'] = form
    return render(request, 'precaution_types.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_precaution_type(request, precaution_type):
    if not is_in_database(precaution_type=precaution_type):
        return http_not_found_page(request)

    context = {'manager': True, 'segment': 'recipe_type', 'delete_precaution_type': precaution_type}
    if request.method == "POST":
        form = DeletePrecautionTypeForm(request.POST)
        if form.is_valid():
            recipe_type = PrecautionType.objects.filter(name=precaution_type)
            try:
                recipe_type.delete()
                return HttpResponseRedirect('/precautions/precaution_types')
            except ProtectedError:
                context.update({'errMsg': '分類使用中，無法刪除。'})
    else:
        form = DeletePrecautionTypeForm()
    context['form'] = form
    return render(request, 'delete_precaution_type.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def upload_precaution(request):
    context = {'segment': 'upload_precaution', 'manager': True}
    if request.method == "POST":
        form = PrecautionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context['Msg'] = f'Success'
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = PrecautionForm()
    context['form'] = form
    return render(request, 'upload_precaution.html', context)