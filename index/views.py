from django.contrib.auth.decorators import login_required
from django.template import loader
from decouple import config
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model


CONTEXT = {
    "PROJECT_TITLE": config('PROJECT_TITLE', default='unnamed'),
    "segment": 'Index',
}


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    User = get_user_model()
    user = User.objects.get(username=request.user)

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

