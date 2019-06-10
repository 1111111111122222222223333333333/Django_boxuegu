import re
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from boxuegu.utils import meiduo_signature
from organization.models import Teacher
from users import constants
from users.forms import RegisterForm,ForgetForm
from .models import UserProfile,EmailVerifyRecord,Banner
from courses.models import Course,CourseOrg
from operation.models import UserMessage, UserFavorite
from operation.models import UserCourse
from django import http
from django.shortcuts import render, redirect
from django.views import View
from celery_tasks.mail.tasks import send_user_email
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
# Create your views here.

#注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        # 调用模版渲染生成表单
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 1、获取前端传递的表单数据
        data = request.POST
        # 2、验证表单数据
        register_form = RegisterForm(data)
        res = register_form.is_valid()  # 验证成功返回True，验证失败返回False
        if res:
            username = data.get('email')
            password = data.get('password')
            user = UserProfile.objects.create_user(username=username,password=password)
            login(request,user)
            response = redirect('/')
            response.set_cookie('username',user.username)
            return response
        # 验证失败，则在注册模板中通过register_form.errors获取错误
        return render(request, 'register.html', {'register_form': register_form})

#登录
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next','/')
        if not all([username, password]):
            return http.HttpResponseBadRequest('参数不完整')
            # 2.2用户名
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseBadRequest('请输入5-20个字符的用户名')
            # 2.3密码
        if not re.match('[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseBadRequest('请输入8-20位的密码')
            # 处理
        user = authenticate(username=username, password=password)
        if user is None:
            # 用户名或密码错误
            return render(request, 'login.html', {
                'loginerror': '用户名或密码错误'
            })
        else:
            # 登录成功，状态保持
            login(request, user)
            # 向cookie中输出用户名，用于在前端提示登录状态
            response = redirect(next_url)
            response.set_cookie('username', user.username, max_age=60 * 60 * 24 * 14)
            return response

#首页
class IndexView(View):
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "all_banners": all_banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })

class SearchView(View):
    def get(self,request,keywords):
        all_courses = Course.objects.all()
        all_orgs =CourseOrg.objects.all()
        all_teachers = Teacher.objects.all()
        # 课程全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))

        # 机构全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 讲师全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords))

#退出
class LogoutView(View):

    def get(self,request):
        logout(request)
        response = redirect('/')
        response.delete_cookie('username')
        return response

#忘记密码
class ForgetpwdView(View):

    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html', {'forget_form': forget_form})
    def post(self, request):
        email = request.POST.get('email')
        user = UserProfile.objects.get(email=email)
        # 发邮件
        # 验证
        if not all([email]):
            return http.JsonResponse('参数不全')
        if not re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.JsonResponse('格式不对')
        token = meiduo_signature.dumps({'user_id': user.id},constants.EXPIRE_EMAIL)
        verify_url = settings.EMAIL_VERIFY_URL + '%s' % token
        response = send_user_email.delay(email, verify_url)
        # 响应
        if response:
            return render(request, 'send_success.html')
        else:
            forget_form = ForgetForm()
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})

#修改密码
class Modify_pwdView(View):
    def get(self,request,active_code):
        # 接收
        # token = request.GET.get('token')
        # 验证
        dict1 = meiduo_signature.loadds(active_code, constants.EXPIRE_EMAIL)
        if dict1 is None:
            return http.HttpResponseBadRequest('激活信息无效，请重新发邮件')
        user_id = dict1.get('user_id')
        # 处理
        try:
            user = UserProfile.objects.get(pk=user_id)
            email = user.email
        except:
            return http.HttpResponseBadRequest('激活信息无效')
        return render(request,'password_reset.html',{'email': email})
    def post(self,request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if not all(['password1','password2']):
            return http.JsonResponse('缺少参数')
        if password1 != password2:
            return http.JsonResponse('密码不一致')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password1):
            return http.HttpResponseBadRequest('密码格式错误')
        user = UserProfile.objects.get(email=email)
        user.set_password(password1)
        user.save()
        return redirect('/')

#用户中心
class UserinfoView(View):

    def get(self,request):
        return render(request, 'usercenter-info.html')

    def post(self,request):
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
        return render(request,'usercenter-info.html',{"status":"success"})

#我的信息
class MymessageView(View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read = True
            unread_messages.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 3)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "messages": messages,
        })

#我的课程
class MycourseView(View):
    def get(self, request):
        courses = UserCourse.objects.all()
        user_courses=[]
        for course in courses:
            user_courses.append(course)
            # aa = course.course
            # bb = aa.course_org
            # user_courses.append({
            #     'course.id':course.id,
            #     'course.image':aa.image,
            #     'course.name':aa.name,
            #     'course.learn_times':aa.learn_times,
            #     'course.students':aa.students,
            #     'course.course_org.name':bb.name
            # })
            return render(request, 'usercenter-mycourse.html', {'user_courses':user_courses,})

#收藏的学校
class Myfav_orgView(View):
    def get(self, request):
        user = request.user
        schools = UserFavorite.objects.filter(fav_type=2, user_id=user.id)
        school_list=[]
        for school in schools:
            orgs = CourseOrg.objects.filter(pk=school.fav_id)
            for org in orgs:
                school_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'org_list': school_list,})

#收藏的老师
class Myfav_teacherView(View):
    def get(self, request):
        user = request.user
        teacher = UserFavorite.objects.filter(fav_type=3, user_id=user.id)
        teacher_list = []
        for teach in teacher:
            teachers = Teacher.objects.filter(pk=teach.fav_id)
            for ter in teachers:
                teacher_list.append(ter)
        return render(request, 'usercenter-fav-teacher.html', {'teacher_list': teacher_list,})

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

#上传图片
class ImageuploadView(View):
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
            return http.JsonResponse({"status": "error", "msg": '头像修改失败'})



