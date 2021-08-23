from django.db import models

"""
Definicion de los modelos de Permiso y Rol
"""

class Permiso(models.Model):
    """
    Implementa la clase de permisos
    """
    nombre = models.CharField(max_length=70, blank=False, null=False)
    """
    tipo 1 = Permisos de administracion
    tipo 2 = Permisos de Proyecto
    """
    tipo = models.IntegerField()

    def __str__(self):
        """
        Metodo que retorna el nombre del permiso actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre


class Rol(models.Model):
    """
    Se definen los campos necesarios para el modelo Rol
    """
    is_unique = models.BooleanField(verbose_name='Es único en el proyecto', default=False)
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
   # permisos = models.ManyToManyField('Permiso', blank=False)
    permisos = models.ManyToManyField('rol.Permiso', blank=False)

    def __str__(self):
        """
        Metodo que retorna el nombre del rol actual
        :return: retorna el valor del campo nombre del objeto
        """
        return self.nombre

    def get_nombres_permisos(self, proyecto=None):
        """
        Metodo que retorna todos los permisos del usuario, con contexto de proyecto o sin
        :param proyecto: Proyecto para el que se solicitan los permisos de usuario segun el rol
        :return: La lista de todos los permisos de administracion mas los permisos del proyecto
                proporcionado o solo los permisos de administracion si no se proporciona proyecto
        """
        permisos = []
            
        for permiso in Permiso.objects.all():
            permisos.append(permiso.nombre)
        return permisos