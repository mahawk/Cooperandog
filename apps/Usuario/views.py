# Django
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError, transaction
from django.contrib.auth import authenticate, login, logout

# Rest
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Modelos
from apps.Usuario.models import Usuario
from django.contrib.auth.models import User
from apps.Adopciones.models import Adopcion
from apps.Adopciones.models import ComentarioAdopcion
from apps.Rescate.models import Rescate
from apps.Rescate.models import ComentarioRescate
from apps.Extravio.models import Extravio
from apps.Extravio.models import ComentarioExtravio
# Serializadores
from apps.Usuario.serializers import UsuarioSerializer
from apps.Usuario.serializers import UserSerializer
from apps.Adopciones.serializers import AdopcionesSerializer
from apps.Adopciones.serializers import ComentarioAdopcionSerializer
from apps.Rescate.serializers import ComentarioRescateSerializer
from apps.Rescate.serializers import RescatesSerializer
from apps.Extravio.serializers import ExtraviosSerializer
from apps.Extravio.serializers import ComentarioExtravioSerializer
from apps.Usuario.serializers import UserAllSerializer

# Utilidades
import re

# Create your views here.
# ==============================================================================
# Subclase de HTTPRESPONSE: Una RespuestHTTP que renderiza su contenido como JSON
# ==============================================================================
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@transaction.atomic
def registro(request):
	if request.method == 'POST':
		nombre= request.POST['nombre']
		username = request.POST['username']
		estado = request.POST['estado']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		imagen = request.FILES['foto']
		if password1 == password2:
			userData = {
				'username': username,
				'password': password1
			}
			serializerUser = UserSerializer(data=userData)
			
			if serializerUser.is_valid():
				usuarioData = {
					'nombre': nombre,
					'estado': estado,
					'foto': imagen
				}
				serializerUsuario = UsuarioSerializer(data=usuarioData)

				if serializerUsuario.is_valid():
					try:
						user = User.objects.create_user(
		                    username=username, 
		                    password=password1
		                )
					except IntegrityError:
						return JSONResponse({
							'userExists': _('!Este correo ya esta registrado¡')
						}, status=400)

					user.save()

					usuario = Usuario.objects.create(user=user, nombre=nombre, estado=estado, foto=imagen)
					usuario.save()
					return JSONResponse({}, status=200)

				return JSONResponse(serializerUsuario.errors, status=400)

			return JSONResponse(serializerUser.errors, status=400)
		else:
			return JSONResponse({
					'password': _('¡Las contraseñas no coinciden!')
				}, status=400)

@csrf_exempt
def inicio_sesion(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		regex = r'[a-z0-9._%+-]+@[a-z0-9.-]+[\\.][a-z]{2,}$'
		if re.match(regex, username):
			user = authenticate(request, username=username, password=password)
			if user:
			    login(request, user)
			    usuario = Usuario.objects.get(user=user)
			    userSerial = UserSerializer(user)
			    usuarioSerial = UsuarioSerializer(usuario)
			    return JSONResponse(
			    	data={
			    		'success': {
				    		'user': userSerial.data,
				    		'usuario': usuarioSerial.data
			    		}
			    	},
			    	status=200
				)
			else:
				return JSONResponse(
					data={
					'error': '¡Usuario o contraseña incorrectos!'
					}, status=400
				)
		else:
			return JSONResponse(
				data={
					'error': '¡Ingrese un correo valido!.\n Ej: puppy@mail.com'
				},
				status=400
			)

@csrf_exempt
def perfil(request, username):
	if request.method == 'GET':
		username = username
		user = User.objects.get(username=username)
		usuario = Usuario.objects.get(user=user)
		userSerial = UserSerializer(user)
		usuarioSerial = UsuarioSerializer(usuario)
		data = {
			'user': userSerial.data,
			'usuario': usuarioSerial.data
		}
		return JSONResponse(data, status=200)

@csrf_exempt
def cantidad_publicaciones(request, username):
	if request.method == 'GET':
		user = User.objects.get(username=username)
		usuario = Usuario.objects.get(user=user)
		contador = 0
		rescates = Rescate.objects.filter(usuario=usuario)
		for rescate in rescates:
			contador += 1
		extravios = Extravio.objects.filter(usuario=usuario)
		for extravio in extravios:
			contador += 1
		adopciones = Adopcion.objects.filter(usuario=usuario)
		for adopcion in adopciones:
			contador += 1
		data = {
			'success': {
				'totalPublicaciones': contador
			}
		}
		return JSONResponse(data, status=200)

@csrf_exempt
def cantidad_comentarios(request, username):
	if request.method == 'GET':
		user = User.objects.get(username=username)
		usuario = Usuario.objects.get(user=user)
		rescates = ComentarioRescate.objects.filter(usuario=usuario)
		contador = 0
		for rescate in rescates:
			contador += 1
		extravios = ComentarioExtravio.objects.filter(usuario=usuario)
		for extravio in extravios:
			contador += 1
		adopciones = ComentarioAdopcion.objects.filter(usuario=usuario)
		for adopcion in adopciones:
			contador += 1
		data = {
			'success': {
				'totalComentarios': contador
			}
		}
		return JSONResponse(data, status=200)

@csrf_exempt
def dias_activo(request, username):
	if request.method == 'GET':
		user = User.objects.get(username=username)
		userSerialized = UserAllSerializer(user)
		data = {
			'success': {
				'user': userSerialized.data
			}
		}
		return JSONResponse(data, status=200)

@csrf_exempt
def publicaciones_usuario(request, username):
	if request.method == 'GET':
		user = User.objects.get(username=username)
		usuario = Usuario.objects.get(user=user)
		adopciones = Adopcion.objects.filter(usuario=usuario.id)
		adopcionesSerialized = AdopcionesSerializer(adopciones, many=True)
		cantidadComAdopcion = []
		for adopcion in adopciones:
			comentariosAdopcion = ComentarioAdopcion.objects.filter(adopcion=adopcion.id) 
			comentariosSerialized = ComentarioAdopcionSerializer(comentariosAdopcion, many=True)
			cantidadComAdopcion.append(len(comentariosSerialized.data))
		rescates = Rescate.objects.filter(usuario=usuario.id)
		rescatesSerialized = RescatesSerializer(rescates, many=True)
		cantidadComRescate = []
		for rescate in rescates:
			comentariosRescate = ComentarioRescate.objects.filter(rescate=rescate.id) 
			comentariosResSerialized = ComentarioRescateSerializer(comentariosRescate, many=True)
			cantidadComRescate.append(len(comentariosResSerialized.data))
		extravios = Extravio.objects.filter(usuario=usuario.id)
		extraviosSerialized = ExtraviosSerializer(extravios, many=True)
		cantidadComExtravio = []
		for extravio in extravios:
			comentariosExtravio = ComentarioExtravio.objects.filter(extravio=extravio.id) 
			comentariosExtSerialized = ComentarioExtravioSerializer(comentariosExtravio, many=True)
			cantidadComExtravio.append(len(comentariosExtSerialized.data))
		data = {
			'success': {
				'adopciones': adopcionesSerialized.data,
				'rescates': rescatesSerialized.data,
				'extravios': extraviosSerialized.data,
				'comentAdopciones': cantidadComAdopcion,
				'comentRescates': cantidadComRescate,
				'comentExtravios': cantidadComExtravio,
			}
		}
		return JSONResponse(data, status=200)

@csrf_exempt
def logout_view(request, username):
	user = User.objects.get(username=username)
	logout(request)
	data = {
		'success': True
	}
	return JSONResponse(data, status=200)

