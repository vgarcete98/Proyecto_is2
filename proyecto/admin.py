from django.contrib import admin
from .models import *


class TeamMemberInLine(admin.TabularInline):
    model = TeamMember

class ProyectoAdmin(admin.ModelAdmin):
    inlines = (TeamMemberInLine,)

admin.site.register(Proyecto,ProyectoAdmin)