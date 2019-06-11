from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^', views.IndexView.as_view()),
    url(r'^org_list/$', views.OrgList.as_view(), name='org_list'),
    url(r'^teacher_list/$', views.TeacherList.as_view(), name='teacher_list'),
    url(r'^teacher_detail/$', views.TeacherDetail.as_view(), name='teacher_detail'),
    url(r'^add_ask/$', views.AddAsk.as_view(), name='add_ask'),
    url(r'^org_home/$', views.OrgHome.as_view(), name='org_home'),
    url(r'^org_desc/$', views.OrgDesc.as_view(), name='org_desc'),
    url(r'^org_course/$', views.OrgCourse.as_view(), name='org_course'),
]