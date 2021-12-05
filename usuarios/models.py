from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from rol.models import *
from proyecto.models import TeamMember

"""
Se definen los estados de un Usuario
"""
ESTADOS_USUARIO = (
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo')
)


class Usuario(AbstractUser):
    """
    Implementa la clase de Usuarios, hereda campos de AbstractUser en la que se
    encuentran campos necesarios como Nombre, Apellido, Contraseña, email.
    """
    estado = models.CharField(max_length=8, choices=ESTADOS_USUARIO, default='Activo')
    ci = models.CharField(max_length=10, null=True, blank=True)
    telefono= models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    permisos = models.ManyToManyField('rol.Permiso', blank=True, verbose_name='Permisos de Administración')
    email = models.EmailField('Email', blank=False, null=False)

    def __str__(self):
        """
        Metodo que retorna el nombre del usuario
        :return: retorna el valor del campo username del objeto
        """
        return self.username

    def get_nombres_permisos(self, proyecto=None):
        """
        Metodo que retorna todos los permisos del usuario, con contexto de proyecto o sin
        :param proyecto: Proyecto para el que se solicitan los permisos de usuario segun el rol
        :return: La lista de todos los permisos de administracion mas los permisos del proyecto
                proporcionado o solo los permisos de administracion si no se proporciona proyecto
        """
        permisos = []
        if self.is_superuser:
            for permiso in Permiso.objects.all():
                permisos.append(permiso.nombre)
        else:
            for permiso in self.permisos.all():
                permisos.append(permiso.nombre)
            if proyecto:
                rol_usuario = None
                try:
                    team_member = TeamMember.objects.get(proyecto=proyecto, usuario=self.pk)
                    rol_usuario = Rol.objects.get(pk=team_member.rol.pk)
                except:
                    pass
                if rol_usuario:
                    for rol in rol_usuario.permisos.all():
                        permisos.append(rol.nombre)
        return permisos