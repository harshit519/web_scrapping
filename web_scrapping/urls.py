"""
URL configuration for web_scrapping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from basic.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/",home,name="home"),
    path("iphone_flipkart/",iphone_flipkart,name="iphone_flipkart"),
    path("samsung_flipkart/",samsung_flipkart,name="samsung_flipkart"),
    path("iphone_amazon/",iphone_amazon,name="iphone_amazon"),
    path("samsung_amazon/",samsung_amazon,name="samsung_amazon"),

    path('login/',login_page,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout_page,name='logout_page'),

  
]
