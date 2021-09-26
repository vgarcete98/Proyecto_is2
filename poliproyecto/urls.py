"""poliproyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls import static
from accounts.views import login, logout
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', login),
    path('logout/', logout),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('accounts/', include('accounts.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('roles/', include('rol.urls')),
    path('proyectos/', include('proyecto.urls')),
]
