from django.contrib import admin

# Register your models here.

from .models import Evento, Usuario, RegistroEvento

admin.site.register(Evento)
admin.site.register(Usuario)
admin.site.register(RegistroEvento)