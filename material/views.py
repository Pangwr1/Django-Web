from django.shortcuts import render, reverse, redirect
from django.http.response import HttpResponse

from user.models import Student, Administrator
from user.constants import INVALID_KIND

# Create your views here.

def get_user(request, kind):
    """

    :param request:
    :param kind: teacher or student
    :return: return Teacher instance or Student instance
    """
    if request.session.get('kind', '') != kind or kind not in ["student", "teacher"]:
        return None

    if len(request.session.get('user', '')) != 10:
        return None

    uid = request.session.get('user')
    grade, number = uid[:4], uid[4:]
    if kind == "student":
        # 找到对应学生
        student_set = Student.objects.filter(grade=grade, number=number)
        if student_set.count() == 0:
            return None
        return student_set[0]
    else:
        # 找到对应老师
        administrator_set = Administrator.objects.filter(department_no=grade, number=number)
    
        if administrator_set.count() == 0:
            return None
        return administrator_set[0]


# Create your views here.
def home(request, kind):
    if kind == "student":
        return student_home(request)
    elif kind == "administrator":
        return administrator_home(request)
    else:
        return HttpResponse(INVALID_KIND)


def administrator_home(request):
    kind = "administrator"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.name,
        "kind": kind
    }

    context = {
        "info": info
    }

    return render(request, 'material/nav.html', context)

def student_home(request):
    kind = "student"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind = kind)

    info = {
        "name": user.name,
        "kind": kind
    }

    context = {
        "info": info
    }

    return render(request, 'material/nav.html', context)
