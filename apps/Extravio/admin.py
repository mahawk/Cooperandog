# Django
from django.contrib import admin

# Modelos
from apps.Extravio.models import Extravio
from apps.Extravio.models import ComentarioExtravio

# Register your models here.
admin.site.register(Extravio)
admin.site.register(ComentarioExtravio)
