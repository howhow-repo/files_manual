from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from employee.views import manager_required
from .forms import PrecautionTypeForm
from .models import PrecautionType


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
