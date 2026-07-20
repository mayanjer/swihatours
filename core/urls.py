"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from swiha.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = "home"),
    path('about/', about, name = "about"),
    path('booking/', booking, name = "booking"),
    path('blog/', blog, name = "blog"),
    path('contact/', contact, name = "contact"),
    path('destinations/', destination, name = 'destinations'),
    path('gallery/', gallery, name = "gallery"),
    path('packages/', packages, name = "packages"),
    
    # these endpoints are used by the fetch api fetch data that updates the DOM
    path('fetch_destinations/', fetch_packages, name="fetch_packages"),
    path('fetch_tour_details/', fetch_tour_details, name = "fetch_tour_details"),
    path('fetch_custom_packages', fetch_custom_packages, name="fetch_custom_packages")
]