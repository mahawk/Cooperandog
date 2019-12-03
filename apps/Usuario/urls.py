# Django
from django.urls import path

from apps.Usuario.views import registro
from apps.Usuario.views import inicio_sesion
from apps.Usuario.views import perfil
from apps.Usuario.views import cantidad_publicaciones
from apps.Usuario.views import cantidad_comentarios
from apps.Usuario.views import dias_activo
from apps.Usuario.views import publicaciones_usuario
from apps.Usuario.views import logout_view

app_name='usuario'
urlpatterns = [
	path('registro/', registro, name='registro'),
	path('login/', inicio_sesion, name='login'),
	path('perfil/<username>/', perfil, name='perfil'),
	path('perfil/cantidad_publicaciones/<username>/', cantidad_publicaciones, name='cantidad_publicaciones'),
	path('perfil/cantidad_comentarios/<username>/', cantidad_comentarios, name='cantidad_comentarios'),
	path('perfil/dias_activo/<username>/', dias_activo, name='dias_activo'),
	path('perfil/publicaciones_usuario/<username>/', publicaciones_usuario, name='publicaciones_usuario'),
	path('logout/<username>/', logout_view, name='logout'),
]
	
