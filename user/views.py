from django.http import HttpResponse
from django.shortcuts import render

from user.constants import INVALID_KIND
from user.forms import StuLoginForm, AdmLoginForm
from user.cbvs import CreateStudentView, CreateAdministratorView

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
    elif request.method == 'GET':
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            data = {'uid': uid, 'password': '12345678'}

            if kind == 'student':
                form = StuLoginForm(data)
            else:
                form = AdmLoginForm(data)
        else:
            if kind == 'student':
                form = StuLoginForm()
            else:
                form = AdmLoginForm()

        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')
    
    return render(request, 'user/login_detail.html', context)

def register(request, kind):
    func = None
    if kind == 'student':
        func = CreateStudentView.as_view()
    elif kind == 'administrator':
        func = CreateAdministratorView.as_view()
    
    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)