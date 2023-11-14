from dataclasses import fields
from decimal import MAX_EMAX
from django import forms
from user.models import Student, Administrator

# 学生登陆信息
class StuLoginForm(forms.Form):
    uid     = forms.CharField(label='学号', max_length=10)
    password= forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)

# 管理员登陆信息
class AdmLoginForm(forms.Form):
    aid     = forms.CharField(label='编号', max_length=10)
    password= forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)

# 学生注册信息
class StuRegisterForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = (
            'grade',
            'name',
            'password',
            'confirm_password',
            'gender',
            'birthday',
            'email',
            'info',
        )

        def clean(self):
            cleaned_data    = super(StuRegisterForm, self).clean()
            password        = cleaned_data.get('password')
            confirm_password= cleaned_data.get('confirm_password')
            if confirm_password != password:
                self.add_error('confirm_password', 'Password does not match.')

# 管理员注册信息
class AdmRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = Administrator
        fields = (
            'grade',
            'name',
            'password',
            'confirm_password',
            'gender',
            'birthday',
            'email',
            'info',
        )

        def clean(self):
            cleaned_data    = super(StuRegisterForm, self).clean()
            password        = cleaned_data.get('password')
            confirm_password= cleaned_data.get('confirm_password')
            if confirm_password != password:
                self.add_error('confirm_password', 'Password does not match.')