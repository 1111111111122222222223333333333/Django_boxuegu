from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.OrgListView.as_view(),name='org_list'),
    url(r'^orghome/(?P<org_id>)\d+$',views.OrgHomeView.as_view(),name='org_home'),
    url(r'^$', views.TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacherdetail/(?P<user_id>)\d+$', views.TeacherDetailView.as_view(), name='teacher_detail'),
    url(r'^$', views.AddfavView.as_view(), name='add_fav'),
    url(r'^orgteacher/(?P<org_id>)\d+$', views.Org_teacherView.as_view(), name='org_teacher'),
    url(r'^orgdesc/(?P<org_id>)\d+$', views.Org_descView.as_view(), name='org_desc'),
    url(r'^orgcourse/(?P<org_id>)\d+$', views.Org_courseView.as_view(), name='org_course'),
]

