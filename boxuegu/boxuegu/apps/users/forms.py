from django import forms
from captcha.fields import CaptchaField

class RegisterForm(forms.Form):

    email=forms.CharField(max_length=20,min_length=5,required=True,label='邮箱')
    password=forms.CharField(max_length=20, min_length=8, required=True,label='密码')
    captcha=CaptchaField(label='验证码')

class ForgetPwdForm(forms.Form):
    email=forms.CharField(max_length=20,min_length=5,required=True,label='邮箱')
    captcha=CaptchaField(label='验证码')
