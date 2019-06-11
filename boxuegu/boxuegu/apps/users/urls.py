from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^index/', views.IndexView.as_view(), name="index"),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^forget/$', views.ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', views.ResetView.as_view(), name='reset_pwd'),
    url(r'^reset/$', views.ResetView.as_view(), name='modify_pwd'),
    url(r'^image/upload/$', views.UploadImageView.as_view(), name='image_upload'),
    # url(r'^info/$', views.UserInfoView.as_view(), name='user_info'),
    url(r'^users/info/$', views.UserInfoView.as_view(), name='user_info'),
    url(r'^mycourse/$', views.MyCourseView.as_view(), name='mycourse'),
    url(r'^myfav/org/$', views.MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav/teacher/$', views.MyFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^myfav/course/$', views.MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^mymessage/$', views.MyMessageView.as_view(), name='mymessage'),

]
