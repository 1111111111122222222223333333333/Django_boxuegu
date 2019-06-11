from django import forms
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    """
        用户注册表单
    """
    nick_name = forms.CharField(max_length=50, min_length=4, label='用户名')
    mobile = forms.CharField(max_length=11, label='手机号')
    email = forms.CharField(max_length=20, min_length=5, required=True, label='邮箱')
    password = forms.CharField(max_length=20, min_length=8, required=True, label='密码')
    # 增加验证码字段
    captcha = CaptchaField(label='验证码')


class LoginForm(forms.Form):
    """
        用户登录表单
    """
    nick_name = forms.CharField(max_length=50, min_length=4, label='用户名')
    # mobile = forms.CharField(max_length=11, required=True, label='手机号')
    # email = forms.CharField(max_length=20, min_length=5, required=True, label='邮箱')
    password = forms.CharField(max_length=20, min_length=6, required=True, label='密码')


class ForgetPwdForm(forms.Form):
    """
        用户忘记密码
    """
    email = forms.CharField(max_length=30, min_length=5, required=True, label='邮箱')
    # 增加验证码字段
    captcha = CaptchaField(label='验证码')

class ForgetPwdForm(forms.Form):
    """
        用户忘记密码
    """
    email = forms.CharField(max_length=30, min_length=5, required=True, label='邮箱')
    # 增加验证码字段
    captcha = CaptchaField(label='验证码')


class UserCoursesForm(forms.Form):
    """
        我的课程
    """
    email = forms.CharField(max_length=20, min_length=5, required=True, label='邮箱')
    password = forms.CharField(max_length=20, min_length=6, required=True, label='密码')
    # mobile = forms.CharField(max_length=11, min_length=11,required=True,label='手机号')
