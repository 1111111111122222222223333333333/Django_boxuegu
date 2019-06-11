import re

from django.conf import settings

from celery_tasks.mail.tasks import send_user_mail
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django import http
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterForm, LoginForm, ForgetPwdForm, UserCoursesForm
from .models import UserProfile, Banner
from courses.models import Course, BannerCourse, CourseOrg
from organization.models import CourseOrg, Teacher, CityDict
from operation.models import UserCourse, UserMessage, UserProfile, UserFavorite, UserAsk
from utils import boxuegu_signature
from . import constants


# 首页
class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all()
        courses = Course.objects.all()
        banner_courses = BannerCourse.objects.all()
        course_orgs = CourseOrg.objects.all()

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


# 注册
class RegisterView(View):
    def get(self, request):
        # 生成表单对象
        register_form = RegisterForm()
        # 调用模板渲染生成表单
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 验证表单数据
        # 获取前端传递的表单数据
        data = request.POST
        register_form = RegisterForm(data)
        result = register_form.is_valid()

        if result:
            # 如果验证成功，则获取清洗后的数据
            username = register_form.cleaned_data['nick_name']
            mobile = register_form.cleaned_data['mobile']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            # 格式验证
            if not re.match(r'^1[345789]\d{9}$', mobile):
                return render(request, 'login.html', {'form_errors': register_form.errors})

            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return render(request, 'login.html', {'form_errors': register_form.errors})

            user = UserProfile.objects.create_user(username=username,
                                                   mobile=mobile,
                                                   email=email,
                                                   password=password,
                                                   )
            user.save()
            login(request, user)
            return render(request, 'index.html')

        return render(request, 'register.html', {'register_form': register_form})


# 登录逻辑
class LoginView(View):
    def get(self, request):
        # 生成表单对象
        login_form = LoginForm()
        # 调用模板渲染生成表单
        return render(request, 'login.html', {'register_form': login_form})

    def post(self, request):
        # 验证表单数据
        # 获取前端传递的表单数据
        data = request.POST
        # 生成表单对象
        login_form = LoginForm(data)
        result = login_form.is_valid()
        # user = request.user

        if result:
            # 如果验证成功
            username = login_form.cleaned_data['nick_name']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {
                    'loginerror': '用户名或密码错误'
                })
            else:
                # 状态保持
                login(request, user)
                # 跳转页面
                # return HttpResponsePermanentRedirect(reverse('index'))
                return redirect('/')
        return render(request, 'login.html', {'form_errors': login_form.errors})


# 登出逻辑
class LogoutView(View):
    def get(self, request):
        # 删sessio
        logout(request)
        # 删cookie
        response = redirect('/')
        response.delete_cookie('username')
        return response


# 忘记密码
class ForgetPwdView(View):

    def get(self, request):
        # 生成表单对象
        forget_form = ForgetPwdForm()
        # 调用模板渲染生成表单
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        # 验证表单数据
        # 获取前端传递的表单数据
        data = request.POST
        forget_form = ForgetPwdForm(data)
        result = forget_form.is_valid()

        if result:
            # 如果验证成功，则获取清洗后的数据
            email = forget_form.cleaned_data['email']
            user = UserProfile.objects.get(email=email)
            # 处理
            # 发邮件
            token = boxuegu_signature.dumps({'user_id': user.id}, constants.EMAIL_EXPIRES)
            verify_url = settings.EMAIL_VERIFY_URL + '%s' % token
            send_user_mail.delay(email, verify_url)

            return render(request, 'send_success.html')

        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 修改密码
class ResetView(View):
    def get(self, request, active_code):
        # 接收
        # token = request.GET.get('token')
        # 验证
        dict1 = boxuegu_signature.loads(active_code, constants.EMAIL_EXPIRES)
        if dict1 is None:
            return http.HttpResponseBadRequest('激活信息无效，请重新发邮件')
        user_id = dict1.get('user_id')
        # 处理
        try:
            user = UserProfile.objects.get(pk=user_id)
            email = user.email
        except:
            return http.HttpResponseBadRequest('激活信息无效')
        return render(request, 'password_reset.html', {'email': email})

    def post(self, request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if not all(['password1', 'password2']):
            return http.JsonResponse('缺少参数')
        if password1 != password2:
            return http.JsonResponse('密码不一致')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password1):
            return http.HttpResponseBadRequest('密码格式错误')
        user = UserProfile.objects.get(email=email)
        user.set_password(password1)
        user.save()
        return redirect('/')


# 用户中心
class UserInfoView(View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        nick_name = request.POST.get('nick_name')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        user = UserProfile.objects.get(email=email)
        user.nick_name = nick_name
        user.birthday = birthday
        user.gender = gender
        user.address = address
        user.mobile = mobile
        user.save()
        return render(request, 'usercenter-info.html', {"status": "success"})


# 更改用户头像
class UploadImageView(View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user = request.user
        image = request.FILES['image']
        user = UserProfile.objects.get(username=user)
        user.image = image
        user.save()
        return http.JsonResponse({
            "status": "success",
            "msg": '头像修改成功'
        })


# 我的课程
class MyCourseView(View):
    def get(self, request):
        user_courses = UserCourse.objects.all()
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


# 课程学校
class MyFavOrgView(View):
    def get(self, request):
        org_list = CourseOrg.objects.all()
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


# 授课教师
class MyFavTeacherView(View):
    def get(self, request):
        teacher_list = Teacher.objects.all()
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


# 公开课程
class MyFavCourseView(View):
    def get(self, request):
        course_list = Course.objects.all()
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


# 我的消息
class MyMessageView(View):
    def get(self, request):
        messages = UserMessage.objects.all()
        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })
