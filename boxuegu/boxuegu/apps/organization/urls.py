from django.conf.urls import url

from . import views
urlpatterns=[
    url('^orglist/$',views.OrgList.as_view(),name='org_list'),
    url('^teacherlist/$',views.OrgList.as_view(),name='teacher_list'),
    url('^addfav/$',views.AddfavView.as_view(),name='add_fav')
]