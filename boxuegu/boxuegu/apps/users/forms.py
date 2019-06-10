from captcha.fields import CaptchaField
from django import forms


class RegisterForm(forms.Form):
    """
        用户注册表单
    """
    email = forms.CharField(max_length=20, min_length=5, required=True,label='用户名')
    password = forms.CharField(max_length=20, min_length=8, required=True,label='密码')
    # 增加验证码字段
    captcha = CaptchaField(label='验证码')

# class UserInfoForm(forms.Form):
#     nick_name = forms.CharField('nick_name')
#     birthday = forms.DateTimeField('birthday')
#     gender = forms.CharField('gender')
#     address = forms.CharField(max_length=20, min_length=1, required=True)
#     mobile = forms.IntegerField(max_length=11, min_length=11, required=True)
#     email = forms.CharField(max_length=20, min_length=5, required=True)

class ImageForm(forms.Form):
    image = forms.ImageField()

class ForgetForm(forms.Form):
    email = forms.CharField(max_length=20, min_length=5, required=True, label='用户名')
    # 增加验证码字段
    captcha = CaptchaField(label='验证码')