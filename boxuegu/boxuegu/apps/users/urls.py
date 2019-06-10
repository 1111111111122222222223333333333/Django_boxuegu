from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    url(r'^login/$',views.LoginView.as_view(),name='login'),
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^logout/$',views.LogoutView.as_view(),name='logout'),
    url(r'^forgetpwd/$',views.ForgetpwdView.as_view(),name='forget_pwd'),
    url(r'^users/info/$',views.UserinfoView.as_view(),name='user_info'),
    url(r'^mymessage/$',views.MymessageView.as_view(),name='mymessage'),
    url(r'^mycourse/$', views.MycourseView.as_view(), name='mycourse'),
    url(r'^myfavorg/$',views.Myfav_orgView.as_view(),name='myfav_org'),
    url(r'^myfavcourse/$',views.Myfav_courseView.as_view(),name='myfav_course'),
    url(r'^myfavteacher/$',views.Myfav_teacherView.as_view(),name='myfav_teacher'),
    url(r'^imageupload/$',views.ImageuploadView.as_view(),name='image_upload'),
    url(r'^reset/(?P<active_code>.*)/$',views.Modify_pwdView.as_view(),name='reset_pwd'),
    url(r'^reset/$',views.Modify_pwdView.as_view(),name='modify_pwd'),
    url(r'^course/list/(?P<keywords>)\d+$',views.SearchView.as_view()),


]



