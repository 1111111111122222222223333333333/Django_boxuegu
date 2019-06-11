import re
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http

from boxuegu.utils import meiduo_signature
from operation.models import UserCourse, UserMessage, UserFavorite
from organization.models import CourseOrg, Teacher
from .models import Banner, UserProfile
from courses.models import Course
from users.forms import RegisterForm, ForgetPwdForm
from celery_tasks.mail.tasks import send_active_mail


# 首页
class IndexView(View):
    def get(self, request):
        banner_list = Banner.objects.all()
        courses = Course.objects.all()

        context = {'all_banners': banner_list,
                   'courses': courses,
                   'banner_courses': courses,
                   'course_org': CourseOrg.objects.all(),

                   }
        return render(request, 'index.html', context)


# 退出
class LogoutView(View):
    def get(self, request):
        logout(request)

        return render(request, 'index.html')


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
        user.brithday = birthday
        user.gender = gender
        user.address = address
        user.mobile = mobile
        user.save()
        return render(request, 'usercenter-info.html', {"status": "success"})


# 注册
class RegisterView(View):
    def get(self, request):

        register_form = RegisterForm()

        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):

        data = request.POST

        register_form = RegisterForm(data)
        res = register_form.is_valid()
        if res:
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            try:
                UserProfile.objects.create_user(username=email, email=email, password=password)
                return redirect('/')
            except:
                return render(request, 'register.html', {'register_form': register_form})
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少参数')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码格式错误')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        login(request, user)

        return redirect(reverse('users:index'))


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        email = request.POST.get('email')
        user = UserProfile.objects.get(email=email)
        # 发邮件
        # 验证
        if not all([email]):
            return http.JsonResponse('参数不全')
        if not re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.JsonResponse('格式不对')
        token = meiduo_signature.dumps({'user_id': user.id}, 600)
        verify_url = settings.EMAIL_VERIFY_URL + '%s' % token
        response = send_active_mail.delay(email, verify_url)
        # 响应
        if response:
            return render(request, 'send_success.html')
        else:
            forget_form = ForgetPwdForm()
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})




            # return render(request,'send_success.html')
            # return render(request,'forgetpwd.html')


# 修改头像
class UploadImageView(View):
    def get(self, request):

        return render(request, 'usercenter-info.html')

    def post(self, request):
        user = request.user
        data = request.FILES
        try:
            user = UserProfile.objects.get(username=user.username)
            user.image = data['image']
            user.save()
            return http.JsonResponse({"status": "success", "msg": '头像修改成功'})
        except:
            return http.JsonResponse({"status": 'error', 'msg': '头像修改失败'})


# 我的消息
class MyMessageView(View):
    def get(self, request):
        all_messages=UserMessage.objects.filter(user=request.user.id)

        #进入后清空未读消息
        all_unread_messages=UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read=True
            unread_messages.save()
        #分页
        try:
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
        p=Paginator(all_messages,3)
        messages=p.page(page)

        return render(request,'usercenter-message.html', {
            "messages": messages,})


# 修改密码
class ResetView(View):
    def get(self, request, active_code):
        # 接收
        # token = request.GET.get('token')
        # 验证
        dict1 = meiduo_signature.loadds(active_code, 60)
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


#我的课程
class MycourseView(View):
    def get(self, request):
        courses=UserCourse.objects.all()
        user_courses=[]
        for course in courses:
            user_courses.append(course)

        return render(request,'usercenter-mycourse.html', {'user_courses':user_courses,})

#收藏的学校
class Myfav_orgView(View):
    def get(self, request):
        user=request.user
        schools=UserFavorite.objects.filter(fav_type=2,user_id=user.id)
        school_list=[]
        for school in schools:
            orgs=CourseOrg.objects.filter(pk=school.fav_id)
            for org in orgs:
                school_list.append(org)
        return render(request,'usercenter-fav-org.html',{'org_list': school_list,})

#收藏老师
class Myfav_teacherView(View):
    def get(self,request):
        user=request.user
        teachers=UserFavorite.objects.filter(fav_type=3,user_id=user.id)
        teacher_list=[]
        for teacher in teachers:
            teacherss=Teacher.objects.filter(pk=teacher.fav_id)
            for ter in teacherss:
                teacher_list.append(ter)

        return render(request,'usercenter-fav-teacher.html',{'teacher_list': teacher_list,})

#收藏的课程
class Myfav_courseView(View):
    def get(self, request):
        user = request.user
        courses = UserFavorite.objects.filter(fav_type=1, user_id=user.id)
        course_list = []
        for course in courses:
            curs = Course.objects.filter(pk=course.fav_id)
            for cur in curs:
                course_list.append(cur)
        return render(request, 'usercenter-fav-course.html',{'course_list':course_list,})

