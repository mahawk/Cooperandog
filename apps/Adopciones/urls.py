# Django
from django.urls import path

# Funciones
from apps.Adopciones.views import adopciones
from apps.Adopciones.views import adopcion_especifico
from apps.Adopciones.views import nueva_adopcion
from apps.Adopciones.views import nueva_adopcion_no_foto
from apps.Adopciones.views import comentar_adopcion
from apps.Adopciones.views import numero_comentarios

app_name='adopcion'
urlpatterns = [
	path('', adopciones, name='adopciones'),
	path('comentarios/', numero_comentarios, name='numero_comentarios'),
	path('adopcion/<id>/', adopcion_especifico, name='detalles'),
	path('nueva_adopcion/<username>/', nueva_adopcion, name='nueva_adopcion'),
	path('nueva_adopcion/no_foto/<username>/', nueva_adopcion_no_foto, name='nueva_adopcion_sin_foto'),
	path('adopcion/comentar/<id>/<username>/', comentar_adopcion, name='comentar_adopcion'),
]