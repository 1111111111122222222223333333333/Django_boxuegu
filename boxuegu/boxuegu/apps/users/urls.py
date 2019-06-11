from django.conf.urls import url
from . views import IndexView,Myfav_courseView,Myfav_teacherView,LogoutView,UserInfoView,RegisterView,LoginView,ForgetPwdView,UploadImageView,MyMessageView,ResetView,MycourseView,Myfav_orgView
urlpatterns=[
    url('^$',IndexView.as_view(),name='index'),
    url('^logout/$',LogoutView.as_view(),name='logout'),
    url('^users/info/$',UserInfoView.as_view(),name='user_info'),
    url('^register/$',RegisterView.as_view(),name='register'),
    url('^login/$',LoginView.as_view(),name='login'),
    url('^forget/$',ForgetPwdView.as_view(),name='forget_pwd'),
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^reset/$', ResetView.as_view(), name='modify_pwd'),
    url(r'^mycourse/$', MycourseView.as_view(), name='mycourse'),
    url(r'^myfavorg/$', Myfav_orgView.as_view(), name='myfav_org'),
    url(r'^myfavteacher/$', Myfav_teacherView.as_view(), name='myfav_teacher'),
    url(r'^myfavcourse/$', Myfav_courseView.as_view(), name='myfav_course'),

]