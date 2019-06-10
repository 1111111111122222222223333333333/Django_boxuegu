"""boxuegu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.global_settings import MEDIA_ROOT
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.static import serve

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/',include(xadmin.site.urls)),#添加新路由
    url(r'^', include('users.urls',namespace='users',app_name ='users')),
    url(r'^', include('operation.urls')),
    url(r'^', include('organization.urls',namespace='org',app_name ='org')),
    url(r'^', include('courses.urls',namespace='courses',app_name='courses')),
    # 图片验证码路由
    url(r'^captcha/', include('captcha.urls')),
    # 静态图片存储路由配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]

