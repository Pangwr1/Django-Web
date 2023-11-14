from django.http import HttpResponse
from django.shortcuts import render

from user.constants import INVALID_KIND
from user.forms import StuLoginForm, AdmLoginForm

# Create your views here.

def home(request):
    return render(request, "user/login_home.html")

def login(request, *args, **kwargs):
    if not kwargs or kwargs.get("kind", "") not in ["student", "administrator"]:
        return HttpResponse(INVALID_KIND)
    
    kind = kwargs['kind']
    context = {'kind': kind}

    if request.method == 'POST':
        if kind == 'student':
            form = StuLoginForm(data=request.POST)
        else:
            form = AdmLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]

            temp = "hello, %s" % uid
            return HttpResponse(temp)
        else:
            context['form'] = form
    else:
        if kind == 'student':
            form = StuLoginForm()
        else:
            form = AdmLoginForm()

        context['form'] = form
    
    return render(request, 'user/login_detail.html', context)