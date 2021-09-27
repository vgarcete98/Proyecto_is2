from django.conf.urls import include, url
from django.urls import path
from . import views
#from userstory.views import *


"""
Definicion de URLs contenidas en proyectos
"""

urlpatterns = [
    #url(r'^$', views.ProjectListView.as_view(),name='project_list'),
    path(route='project_list', view = views.ProjectListView(), name = 'project_list'),
    #url(r'^create/$', views.CreateProjectView.as_view(), name='create_project'),
    path(route='create_project', view = views.CreateProjectView.as_view(), name = 'create_project'),
    path(route='modificar/<int:pk_proyecto>/', view=views.UpdateProjectView.as_view(), name='update_project'),
    path(route='ver/<int:pk>/', view=views.VerProyectoDetailView.as_view(), name='ver_project')
    #url(r'^definiciones/$', views.OptionsListView.as_view(), name='options_project'),
    #path(route='definiciones/<int:pk_proyecto>/', view=views.UpdateOptionsView.as_view(), name='update_options'),
    #path('definiciones/<int:pk_proyecto>/flujos/',include('flujo.urls')),
    #path('definiciones/<int:pk_proyecto>/tipoUserStory/',include('tipoUserStory.urls'), name='user_story_type_list'),
    #path(route='definiciones/<int:pk_proyecto>/asignarRoles/', view=views.UpdateTeamMemberView.as_view(), name='update_roles_proyecto'),
    #url(r'^ejecuciones/$', views.EjecucionListView.as_view(), name='options_project'),
    #path(route='ejecuciones/<int:pk_proyecto>/', view=views.UpdateEjecucionView.as_view(), name='update_ejecucion'),
    #path('ejecuciones/<int:pk_proyecto>/userstories/', include('userstory.urls')),
    #path(route='ejecuciones/<int:pk_proyecto>/productbacklog/',view=ProductBacklogListView.as_view(), name = 'product_backlog'),
    #path('ejecuciones/<int:pk_proyecto>/sprints/', include('sprint.urls')),
    #path(route='ejecuciones/<int:pk_proyecto>/productbacklogpdf/', view=ProductBacklogPDF.as_view(), name="reporte_pb"),
    #path(route='ejecuciones/<int:pk_proyecto>/horastrabajadas/', view=views.HorasTrabajadasPDF.as_view(), name="horas_trabajadas")
]