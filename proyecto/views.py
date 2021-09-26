from django.views.generic import ListView, CreateView, UpdateView, DetailView
from poliproyecto import settings
from .forms import *
from proyecto.forms import CreateProjectForm, UpdateProjectForm
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
#from sprint.models import *
#from flujo.models import *
from django.utils import timezone
#from userstory.models import *
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
#from reportlab.pdfgen import canvas
import locale
from django.views.generic import View
"""from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import (
        Paragraph,
        Table,
        SimpleDocTemplate,
        Spacer,
        TableStyle,
        Paragraph,
        Image)

"""
"""
Vistas del Proyecto
"""

@method_decorator(login_required, name='dispatch')
class VerProyectoDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto/ver_proyecto.html'

    def get(self,request,*args,**kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(proyecto=self.object.pk)
        context['title'] = "Ver Proyecto " + str(self.object.pk)
        context['direccion'] = {}
        context['direccion']['Proyectos'] = (1, '/proyectos/')
        context['direccion']['Ver: ' + self.object.nombre] = (2, '/proyectos/ver/' + str(self.object.pk) + '/')
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser visualizado
        :param queryset:
        :return: Retorna el proyecto a ser visualizado
        """
        return Proyecto.objects.get(pk=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class ProjectListView(LoginRequiredMixin, ListView):
    """
    Clase de la vista de la lista de Proyectos
    """
    template_name = 'proyecto/list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object_list = Proyecto.objects.all()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(object_list=self.object_list, permisos=permisos))


    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Administración de Proyectos"
        context['direccion'] = {}
        context['direccion']['Proyectos'] = (1,'/proyectos/')
        return context


@method_decorator(login_required, name='dispatch')
class CreateProjectView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Clase de la vista para la creacion de un nuevo Proyecto
    """
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    success_url = '/proyectos/project_list'
    form_class = CreateProjectForm
    success_message = 'Se ha creado el proyecto'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['title'] = "Crear Proyecto"
        context['obs'] = "Obs: El proyecto se crea por defecto en estado pendiente, debe iniciar el proyecto manualmente"
        context['direccion'] = {}
        context['direccion']['Proyectos'] = (1, '/proyectos/')
        context['direccion']['Crear Proyecto'] = (2, '/proyectos/create/')
        return context

    def post(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        self.object = None
        permisos = request.user.get_nombres_permisos()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)

        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset, permisos)

    def form_valid(self, form, team_member_formset):
        """
        Metodo ejecutado luego de verificar que el formulario recibido en la
        consulta POST es valido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion al sucess_url de la clase
        """
        self.object = form.save()
        team_member_formset.instance = self.object
        team_member_formset.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, team_member_formset, permisos):
        """
        Metodo que se ejecuta si el formulario recibido en la consulta POST
        es invalido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion a la pagina actual con los errores de validacion
        """
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        if team_member_formset.rol_doble:
            fs_error = "Solo puede existir un "+str(team_member_formset.rol_doble.nombre)
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, team_members=team_member_formset, permisos=permisos))


@method_decorator(login_required, name='dispatch')
class UpdateProjectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Clase de la vista para la modificacion de un Proyecto
    """
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/project_list'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_members = TeamMember.objects.filter(proyecto=self.object).order_by('pk')
        tm_data = []
        for tm in team_members:
            d = {'usuario': tm.usuario,
                 'rol': tm.rol}
            tm_data.append(d)
        TeamMemberFormSet = inlineformset_factory(Proyecto, TeamMember, form=TeamMemberForm, extra=len(tm_data))
        team_member_formset = TeamMemberFormSet(initial=tm_data)
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Proyecto " + str(self.object.pk)
        context['direccion'] = {}
        context['direccion']['Proyectos'] = (1, '/proyectos/')
        context['direccion']['Modificar: '+self.object.nombre] = (2, '/proyectos/modificar/'+str(self.object.pk)+'/')
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser modificado
        :param queryset:
        :return: El proyecto a ser modificado
        """
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def post(self,request,*args,**kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        permisos = request.user.get_nombres_permisos()
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset, permisos)

    def form_valid(self, form, team_member_formset):
        """
        Metodo ejecutado luego de verificar que el formulario recibido en la consulta
        POST es valido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion al sucess_url de la clase
        """
        self.object = form.save()
        team_member_formset.instance = self.object
        TeamMember.objects.filter(proyecto=self.object).delete()
        team_member_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, team_member_formset, permisos):
        """
        Metodo que se ejecuta si el formulario recibido en la consulta POST
        es invalido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion a la pagina actual con los errores de validacion
        """
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        if team_member_formset.rol_doble:
            fs_error = "Solo puede existir un "+str(team_member_formset.rol_doble.nombre)
        return self.render_to_response(self.get_context_data(permisos=permisos, fs_error=fs_error, form=form, team_members=team_member_formset))


"""
Vistas de Definiciones de Proyecto
"""

@method_decorator(login_required, name='dispatch')
class OptionsListView(LoginRequiredMixin, ListView):
    """
    Clase de la vista de la lista de definiciones de un proyecto existente
    """
    template_name = 'proyecto/opciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get(self,request,*args,**kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object_list = Proyecto.objects.all()
        visibles = []
        for proyecto in self.object_list:
            permisos_proyecto = request.user.get_nombres_permisos(proyecto=proyecto.pk)
            if 'Ver Definiciones de Proyecto' in permisos_proyecto:
                visibles.append(proyecto)
        visibles.sort(key=lambda x: x.pk, reverse=True)
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(visibles=visibles, permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Definiciones de Proyectos"
        context['direccion'] = {}
        context['direccion']['Definiciones'] = (1, '/definiciones/')
        return context


@method_decorator(login_required, name='dispatch')
class UpdateOptionsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Clase de la vista para modificacion de las definiciones de proyecto
    """
    template_name = 'proyecto/options.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/opciones/'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self,request,*args,**kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_members = TeamMember.objects.filter(proyecto=self.object).order_by('pk')
        tm_data = []
        for tm in team_members:
            d = {'usuario': tm.usuario,
                 'rol': tm.rol}
            tm_data.append(d)
        TeamMemberFormSet = inlineformset_factory(Proyecto, TeamMember, form=TeamMemberForm,extra=len(tm_data))
        team_member_formset = TeamMemberFormSet(initial=tm_data)
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Definicion "
        context['direccion'] = {}
        context['direccion']['Definiciones'] = (1, '/proyectos/definiciones/')
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['direccion'][proyecto.nombre] = (1, '/proyectos/definiciones/'+str(proyecto.pk)+'/')
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser modificado
        :param queryset:
        :return: El proyecto a ser modificado
        """
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def post(self,request,*args,**kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
        """
        Metodo ejecutado luego de verificar que el formulario recibido en la consulta
        POST es valido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion al sucess_url de la clase
        """
        self.object = form.save()
        team_member_formset.instance = self.object
        TeamMember.objects.filter(proyecto=self.object).delete()
        team_member_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,team_member_formset):
        """
        Metodo que se ejecuta si el formulario recibido en la consulta POST
        es invalido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion a la pagina actual con los errores de validacion
        """
        return self.render_to_response(self.get_context_data(form=form, team_members=team_member_formset))


"""
Vistas de Ejecucion
"""
@method_decorator(login_required, name='dispatch')
class UpdateTeamMemberView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Clase de la vista para la modificacion del Team Member
    """
    template_name = 'proyecto/asignacion_roles.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '../'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_members = TeamMember.objects.filter(proyecto=self.object).order_by('pk')
        tm_data = []
        for tm in team_members:
            d = {'usuario': tm.usuario,
                 'rol': tm.rol}
            tm_data.append(d)
        TeamMemberFormSet = inlineformset_factory(Proyecto, TeamMember, form=TeamMemberForm, extra=len(tm_data))
        team_member_formset = TeamMemberFormSet(initial=tm_data)
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Asignar Roles"
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser visualizado
        :param queryset:
        :return: Retorna el proyecto a ser modificado
        """
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def post(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
        """
        Metodo que se ejecuta si el formulario recibido en la consulta POST
        es valido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion a la direccion definida en el atributo success_url de la clase
        """
        self.object = form.save()
        team_member_formset.instance = self.object
        TeamMember.objects.filter(proyecto=self.object).delete()
        team_member_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, team_member_formset):
        """
        Metodo que se ejecuta si el formulario recibido en la consulta POST
        es invalido
        :param form: formulario a ser guardado
        :param team_member_formset: grupo de team members del proyecto
        :return: redireccion a la pagina actual con los errores de validacion
        """
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        if team_member_formset.rol_doble:
            fs_error = "Solo puede existir un "+str(team_member_formset.rol_doble.nombre)
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, team_members=team_member_formset))
