# Django
from django.urls import path

# Funciones
from apps.Rescate.views import rescates
from apps.Rescate.views import numero_comentarios
from apps.Rescate.views import rescate_especifico
from apps.Rescate.views import comentar_rescate
from apps.Rescate.views import nuevo_rescate
# from apps.Rescate.views import nuevo_rescate_no_foto

app_name='rescate'
urlpatterns = [
	path('', rescates, name='rescates'),
	path('comentarios/', numero_comentarios, name='numero_comentarios'),
	path('rescate/<id>/', rescate_especifico, name='detalles'),
	path('nuevo_rescate/<username>/', nuevo_rescate, name='nuevo_rescate'),
	# path('nuevo_rescate/no_foto/<username>/', nuevo_rescate_no_foto, name='nuevo_rescate_sin_foto'),
	path('rescate/comentar/<id>/<username>/', comentar_rescate, name='comentar_rescate'),
]