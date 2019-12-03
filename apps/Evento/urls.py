# Django
from django.urls import path

# Funciones
from apps.Evento.views import  eventos
from apps.Evento.views import  evento_especifico

app_name='eventos'
urlpatterns = [
	path('',eventos,name='eventos'),
	path('evento/<id>/',evento_especifico,name='evento_especifico'),
]