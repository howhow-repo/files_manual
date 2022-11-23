import os

from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from employee.views import manager_required, set_org_data_in_form_initial
from yayoi_recipe.views import http_not_found_page, is_manager, remove_document
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


def delete_recipe_related_file(precaution_instance):
    img_path = precaution_instance.cover.name
    file_path = precaution_instance.file.name
    if os.path.isfile(img_path):
        os.remove(img_path)
    if os.path.isfile(file_path):
        os.remove(file_path)


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
                return HttpResponseRedirect(reverse('precaution_types'))
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
            p.doc_type = '無'

    return render(request, 'list_precautions.html', context)


@require_http_methods(["GET"])
@login_required(login_url="/login/")
def precaution_detail(request, precaution_type, precaution_name):

    context = {'segment': 'precaution'}
    if is_manager(request):
        context['manager'] = True

    precaution = Precaution.objects.filter(name=precaution_name).first()

    if not precaution or precaution.type.name != precaution_type:
        return http_not_found_page(request)

    context['precaution'] = precaution
    context['precaution_type'] = precaution_type
    return render(request, 'precaution_detail.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def update_percaution(request, precaution_type, precaution_name):
    precaution_instance = Precaution.objects.filter(name=precaution_name).first()
    if not precaution_instance or precaution_instance.type.name != precaution_type:
        return http_not_found_page(request)
    context = {'segment': 'precaution', 'manager': True, 'precaution_name': precaution_name,
               'precaution_type': precaution_type}
    old_file_path = precaution_instance.file.name
    old_img_path = precaution_instance.cover.name

    if request.method == "POST":
        form = PrecautionForm(request.POST, request.FILES, instance=precaution_instance)
        if form.is_valid():
            if 'cover' in form.changed_data:
                remove_document(old_img_path)

            if 'file' in form.changed_data:
                remove_document(old_file_path)
            form.save()
            return HttpResponseRedirect(reverse('list_precautions', args=('all',)))
    else:
        form = PrecautionForm()

    form = set_org_data_in_form_initial(precaution_instance, form, ['cover', 'file'])
    context['form'] = form
    return render(request, 'edit_precaution.html', context)


@manager_required
@require_http_methods(["GET", "POST"])
@login_required(login_url="/login/")
def delete_percaution(request, precaution_type, precaution_name):
    precaution_instance = Precaution.objects.filter(name=precaution_name).first()
    if not precaution_instance or precaution_instance.type.name != precaution_type:
        return http_not_found_page(request)
    context = {'segment': 'precaution', 'manager': True, 'delete_precaution': precaution_name,
               'precaution_type': precaution_type}
    if request.method == "POST":
        form = DeletePrecautionTypeForm(request.POST)
        if form.is_valid() and form['confirm'].value() == 'yes':
            delete_recipe_related_file(precaution_instance)
            precaution_instance.delete()
            return HttpResponseRedirect(reverse('list_precautions', args=('all',)))
    else:
        form = DeletePrecautionTypeForm()
    context['form'] = form
    return render(request, 'delete_precaution.html', context)
