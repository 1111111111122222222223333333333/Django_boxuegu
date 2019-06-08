from django import forms


class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    username = forms.CharField(max_length=20, min_length=5, required=True, label='用户名')
    password = forms.CharField(max_length=20, min_length=8, required=True, label='密码')
    mobile = forms.CharField(max_length=11, min_length=11, required=True, label='手机号')
