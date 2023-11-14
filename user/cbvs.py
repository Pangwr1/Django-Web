from multiprocessing import context
from pydoc import cram
from django.shortcuts import reverse, redirect
from django.urls import is_valid_path
from django.views.generic import CreateView, UpdateView

from user.models import Student, Administrator
from user.forms import StuRegisterForm, AdmRegisterForm, StuUpdateForm

import random



class CreateStudentView(CreateView):
    model = Student
    form_class = StuRegisterForm
    template_name = 'user/register.html'
    success_url = 'login'


    def form_valid(self, form):
        grade = form.cleaned_data["grade"]
        student_set = Student.objects.filter(grade=grade).order_by("-number")
        
        if student_set.count() > 0:
            last_student = student_set[0]
            new_number = str(int(last_student.number) + 1)
            new_number = "0" * (6 - len(new_number)) + new_number
        else:
            new_number = "000001"
        
        new_student = form.save(commit=False)
        new_student.number = new_number
        new_student.save()
        form.save_m2m()

        self.object = new_student

        uid = grade + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'student'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))

    
    def get_context_data(self, **kwargs):
        context = super(CreateStudentView, self).get_context_data(**kwargs)
        context['kind'] = 'student'

        return context



class CreateAdministratorView(CreateView):
    model = Administrator
    form_class = AdmRegisterForm
    template_name = 'user/register.html'
    success_url = 'login'


    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        grade = form.cleaned_data["grade"]
        administrator_set = Student.objects.filter(grade=grade).order_by("-number")
        
        if administrator_set.count() > 0:
            last_administrator = administrator_set[0]
            new_number = str(int(last_administrator.number) + 1)
            new_number = "0" * (6 - len(new_number)) + new_number
        else:
            new_number = "000001"
        
        new_administrator = form.save(commit=False)
        new_administrator.number = new_number
        new_administrator.save()
        form.save_m2m()

        self.object = new_administrator

        uid = grade + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'administrator'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))

    def get_context_data(self, **kwargs):
        context = super(CreateAdministratorView, self).get_context_data(**kwargs)
        context['kind'] = 'administrator'

        return context



class UpdateStudentView(UpdateView):
    model = Student
    form_class = StuUpdateForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "student"
        return context

    def get_success_url(self):
        return reverse("material", kwargs={"kind": "student"})



class UpdateAdministratorView(UpdateView):
    model = Administrator
    form_class = AdmRegisterForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateAdministratorView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "administrator"
        return context

    def get_success_url(self):
        return reverse("material", kwargs={"kind": "administrator"})

