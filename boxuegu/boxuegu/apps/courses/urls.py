from django.conf.urls import url
from . import views
urlpatterns=[
    url('^courselist/$',views.CouresListView.as_view(),name='course_list')
]