from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,login as auth_login,
    logout as auth_logout
)
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

"""
Vista del Login y Logout
"""


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='accounts/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Muestra la vista de login y maneja los datos enviados para loguearse
    :param request: consulta recibida
    :param template_name: nombre del template que utiliza la vista
    :param redirect_field_name: nombre del campo para redireccion
    :param authentication_form: formulario de autenticacion
    :param current_app: aplicacion actual
    :param extra_context: diccionario de datos adicionales que deben visualizarse en la vista
    :return:
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    error = ""
    if request.user.is_authenticated:
        if not is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return HttpResponseRedirect(redirect_to)

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
        else:
            error = "El usuario no existe o la contraseña es incorrecta"
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'error': error,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def logout(request):
    """
    Vista para redireccion a la pagina de login luego de cerrar sesión
    :param request: consulta recibida
    :return: redireccion a la pagina de login luego de cerrar sesión
    """
    auth_logout(request)
    return HttpResponseRedirect('/')