from decimal import MAX_EMAX
from django import forms
from user.models import Student, Administrator

class StuLoginForm(forms.Form):
    uid     = forms.CharField(label='学号', max_length=10)
    password= forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)

class AdmLoginForm(forms.Form):
    aid     = forms.CharField(label='编号', max_length=10)
    password= forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)