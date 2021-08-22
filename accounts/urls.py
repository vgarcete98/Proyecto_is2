from django.conf.urls import url
from . import views
from poliproyecto.views import home
"""
URL para el login, y para cuando se loguea
"""

urlpatterns = [
	url(r'^$', home),
	url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
]