# Django
from django.urls import path

from apps.Extravio.views import nuevo_extravio
from apps.Extravio.views import extravios
from apps.Extravio.views import numero_comentarios
from apps.Extravio.views import extravio_especifico
from apps.Extravio.views import comentar_extravio

app_name='extravio'
urlpatterns = [
	path('', extravios, name='extravios'),
	path('comentarios/', numero_comentarios, name='numero_comentarios'),
    path('nuevo_extravio/<username>/', nuevo_extravio, name='nuevo_extravio'),
    path('extravio/<id>/', extravio_especifico, name='extravio_especifico'),
    path('extravio/<id>/', extravio_especifico, name='extravio_especifico'),
	path('extravio/comentar/<id>/<username>/', comentar_extravio, name='comentar_extravio'),
]