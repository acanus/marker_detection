"""marker_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import webcam.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name="home"),
    path('setting/', views.setting,name="setting"),
    path('history/', views.history,name="history"),
    path('history/clear_all_image', views.clear_all_image,name="clear_all_image"),
    path('setting/set_record_parameter', views.set_record_parameter,name="set_record_parameter"),
    path('set_parameter', views.set_parameter,name="set_inspection_parameter"),
    path('setting/get_record_parameter', views.get_record_parameter,name="get_record_parameter"),
    path('get_parameter', views.get_parameter,name="get_inspection_parameter"),
    path('set_online', views.set_online ,name='set_online'),
    path('set_offline', views.set_offline,name='set_offline' ),
    path('get_total', views.get_total),
    path('reset_counter', views.reset_counter),
    path('setting/last_image', views.last_image, name="last-image"),
    path('setting/get_image_template_cropped', views.get_image_template_cropped,name="template_image_cropped"),
    path('setting/get_image_template', views.get_image_template, name="image-template"),
    path('setting/set_current_as_template', views.set_current_image_as_template, name="set_current_as_image-template"),
    path('setting/update_template', views.update_template, name="update-template"),
    path('video_feed/', views.video_feed, name="video-feed"),
    path('video_feed_defect/', views.video_feed_defect, name="video-feed-defect")
]


