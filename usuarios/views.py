from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


@method_decorator(login_required, name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    """
    Clase de la vista de la lista de Usuarios
    """
    template_name = 'usuarios/list.html'
    model = Usuario
    queryset = Usuario.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object_list = Usuario.objects.all()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Usuarios"
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1,'/usuarios/')
        return context


@method_decorator(login_required, name='dispatch')
class CreateUserView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Clase de la vista para la creacion de un Usuario
    """
    template_name = 'usuarios/user.html'
    model = Usuario
    success_url = '/usuarios/user_list'
    form_class = CreateUserForm
    success_message = 'Se ha creado el usuario'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = None
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Usuario"
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1, '/usuarios/')
        context['direccion']['Crear Usuario'] = (2, '/usuarios/create/')
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
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        permisos = request.user.get_nombres_permisos()
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(permisos=permisos,form=form))


@method_decorator(login_required, name='dispatch')
class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Clase de la vista para la modificacion de un Usuario
    """
    template_name = 'usuarios/user.html'
    model = Usuario
    form_class = UpdateUserForm
    success_url = '/usuarios/'
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
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Usuario " + str(self.object.pk)
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1,'/usuarios/')
        context['direccion']['Modificar: '+self.object.username] = (2,'/usuarios/modificar/'+str(self.object.pk)+'/')
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser modificado
        :param queryset:
        :return: Retorna el usuario a ser modificado
        """
        return Usuario.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        self.object = self.get_object()
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        permisos = request.user.get_nombres_permisos()
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(permisos=permisos,form=form))


@method_decorator(login_required, name='dispatch')
class VerUserDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    """
    Clase de la vista de los detalles de un Usuario
    """
    model = Usuario
    template_name = 'usuarios/ver_user.html'

    def get(self, request, *args, **kwargs):
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
        context['title'] = "Ver Usuario " + str(self.object.pk)
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1, '/usuarios/')
        context['direccion']['Ver: ' + self.object.username] = (2, '/usuarios/ver/' + str(self.object.pk) + '/')
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser visualizado
        :param queryset:
        :return: Retorna el usuario a ser visualizado
        """
        return Usuario.objects.get(pk=self.kwargs['pk'])