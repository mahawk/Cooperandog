# Django
from django.contrib import admin

# Modelos
from apps.Rescate.models import Rescate
from apps.Rescate.models import ComentarioRescate

# Register your models here.
admin.site.register(Rescate)
admin.site.register(ComentarioRescate)