# Django
from django.contrib import admin

# Modelos
from apps.Adopciones.models import Adopcion
from apps.Adopciones.models import ComentarioAdopcion

# Register your models here.
admin.site.register(Adopcion)
admin.site.register(ComentarioAdopcion)
