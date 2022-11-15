from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from employee.views import manager_required
from yayoi_recipe.views import http_not_found_page, is_manager
from doc_handle.views import video_extension, doc_extension
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


def set_data_type(precaution: Precaution):
    if not precaution.file:
        return
    file_extension = precaution.file.name.split('.')[-1]
    if file_extension in video_extension:
        precaution.doc_type = '影片'
    elif file_extension in doc_extension:
        precaution.doc_type = file_extension.upper()
    precaution.save()


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
            precaution = Precaution.objects.get(name=form.data['name'])
            set_data_type(precaution)
            context['Msg'] = f'Success'
        else:
            context['errMsg'] = 'Form is not valid'
    else:
        form = PrecautionForm()
    context['form'] = form
    return render(request, 'upload_precaution.html', context)


@require_http_methods(["GET"])
@login_required(login_url="/login/")
def list_precautions(request, precaution_type: str = 'all'):
    context = {'segment': 'precaution'}
    if is_manager(request):
        context['manager'] = True
    if precaution_type == 'all':
        context['precaution'] = Precaution.objects.all()
    else:
        context['precaution'] = Precaution.objects.filter(type__name=precaution_type)

    if not (context['precaution']):
        context['empty'] = True

    for p in context['precaution']:
        if not p.doc_type:
            p.doc_type = 'File'

    return render(request, 'list_precautions.html', context)


@require_http_methods(["GET"])
@login_required(login_url="/login/")
def percaution_detail(request, precaution_name):

    context = {'segment': 'precaution'}
    if is_manager(request):
        context['manager'] = True

    precaution = Precaution.objects.get(name=precaution_name)
    if not precaution:
        return http_not_found_page(request)
    context['precaution'] = precaution
    return render(request, 'precaution_detail.html', context)


@manager_required
@require_http_methods(["GET"])
@login_required(login_url="/login/")
def update_percaution(request, precaution_name):
    context = {'segment': 'precaution'}
    if is_manager(request):
        context['manager'] = True
    precaution = Precaution.objects.get(name=precaution_name)
    if not precaution:
        return http_not_found_page(request)



