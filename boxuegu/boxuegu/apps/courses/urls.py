from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^', views.IndexView.as_view()),
    url(r'^course_list/$', views.CoursesList.as_view(), name='course_list'),
    url(r'^course_detail/$', views.CoursesDetail.as_view(), name='course_detail'),
    url(r'^course_info/$', views.CoursesInfo.as_view(), name='course_info'),
]

