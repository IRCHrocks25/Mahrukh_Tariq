from django.contrib import admin
from django.urls import path, include
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('myApp.dashboard_urls')),
    path('blog/<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
    path('', views.home, name='home'),
]
