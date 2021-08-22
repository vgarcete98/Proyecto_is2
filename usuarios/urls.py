from django.conf.urls import url
from django.urls import path
#from . import views
from usuarios import views
from django.views.generic import *
"""
URL para Usuarios: crear, listar, modificar, ver
"""
urlpatterns = [
    #url(r'^$', views.UserListView.as_view(),name='user_list'),
    path(route='user_list', view = views.UserListView.as_view(), name = 'user_list'),
    path(route='create_user', view= views.CreateUserView.as_view(), name ='create_user'),
	#url(r'^create/$', views.CreateUserView.as_view(), name='create_user'),
	path(route='modificar/<int:pk>/', view=views.UpdateUserView.as_view(), name='update_user'),
	path(route='ver/<int:pk>/', view=views.VerUserDetailView.as_view(), name='ver_user')
]