from django.shortcuts import render
from django.views import View
from .forms import RegisterForm


class RegisterView(View):
    def get(self, request):
        # 使用django自带表单
        # 1.生成表单对象
        register_form = RegisterForm()
        # 2.渲染页面
        return render(request, 'register.html', {'register_form': register_form})
