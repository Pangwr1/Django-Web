from audioop import reverse
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render

from user.models import Student, Administrator
from user.constants import INVALID_KIND
from user.forms import StuLoginForm, AdmLoginForm
from user.cbvs import CreateStudentView, CreateAdministratorView, UpdateAdministratorView, UpdateStudentView

# Create your views here.

def home(request):
    return render(request, "user/login_home.html")

def register_home(request):
    return render(request, "user/register_home.html")

def login(request, kind):
    if kind not in ["student", "administrator"]:
        return HttpResponse(INVALID_KIND)
    
    if request.method == 'POST':
        if kind == 'student':
            form = StuLoginForm(data=request.POST)
        else:
            form = AdmLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]

            if len(uid) != 10:
                form.add_error("uid", "账号必须为 10 位数")
            else:
                grade, number = uid[:4], uid[4:]
                if kind == "student":
                    object_set = Student.objects.filter(grade=grade, number=number)
                else:
                    object_set = Administrator.objects.filter(grade=grade, number=number)

                if object_set.count() == 0:
                    form.add_error("uid", "账号不存在")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.password:
                        form.add_error("uid", "密码不正确")
                    else:
                        request.session['kind'] = kind
                        request.session['user'] = uid
                        request.session['id'] = user.id

                        return redirect("material", kind=kind)

            return render(request, 'user/login_detail.html', {'form': form, 'kind': kind})
    else:
        context = {'kind': kind}
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


def logout(request):
    if request.session.get("kind", ""):
        del request.session["kind"]
    if request.session.get("user", ""):
        del request.session["user"]
    if request.session.get("id", ""):
        del request.session["id"]
    return redirect("login")


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

def update(request, kind):
    func = None
    if kind == 'student':
        func = UpdateStudentView.as_view()
    elif kind == 'administrator':
        func = UpdateAdministratorView.as_view()
    else:
        return HttpResponse(INVALID_KIND)
    
    pk = request.session.get("id")
    if pk:
        context = {
            "name": request.session.get("name", ""),
            "kind": request.session.get("kind", ""),
        }
        return func(request, pk=pk, context=context)
    
    return redirect("login")