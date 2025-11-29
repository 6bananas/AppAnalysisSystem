"""
URL configuration for AppAnalysisSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_icon', views.get_icon),
    path('get_messages', views.get_messages),
    path('apk/save', views.download_apk_from_link),
    path('upload/apkFile', views.save_upload_apk),
    path('upload/qrcode', views.download_apk_from_qr),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('user/info', views.get_info),
    path('get_pie_chart1', views.get_pie_chart1),
    path('get_bar_chart', views.get_bar_chart),
]
