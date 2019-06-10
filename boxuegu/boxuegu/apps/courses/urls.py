from django.conf.urls import url
from . import views

app_name='courses'
urlpatterns = [
    url(r'^courselist/$',views.CourseListView.as_view(),name='course_list'),
    url(r'^courseinfo/(?P<couser_id>)\d+$',views.Course_infoView.as_view(),name='course_info'),
    url(r'^course/(?P<couser_id>)\d+$',views.CourseDetailView.as_view(),name='course_detail'),
]

