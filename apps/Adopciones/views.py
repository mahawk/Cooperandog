# Django
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

# Rest
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Modelos
from django.contrib.auth.models import User
from apps.Usuario.models import Usuario
from apps.Adopciones.models import Adopcion
from apps.Adopciones.models import ComentarioAdopcion

# Serializers
from apps.Adopciones.serializers import AdopcionSerializer
from apps.Adopciones.serializers import AdopcionesSerializer
from apps.Adopciones.serializers import ComentarioAdopcionSerializer

# Create your views here.
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def adopciones(request):
	if request.method == 'GET':
		adopciones = Adopcion.objects.all()
		adopcionesSerialized = AdopcionesSerializer(adopciones, many=True)
		data = {
			'adopciones': adopcionesSerialized.data,
		}
		return JSONResponse(data, status=200)

@csrf_exempt
def numero_comentarios(request):
    if request.method == 'GET':
        adopciones = Adopcion.objects.all()
        cantidadCom = []
        for adopcion in adopciones:
            comentariosAdopcion = ComentarioAdopcion.objects.filter(adopcion=adopcion) 
            comentariosSerialized = ComentarioAdopcionSerializer(comentariosAdopcion, many=True)
            cantidadCom.append(len(comentariosSerialized.data))
        data = {
            'comentarios': cantidadCom
        }
        return JSONResponse(data, status=200)


@csrf_exempt
def adopcion_especifico(request, id):
    if request.method == 'GET':
        adopcion = Adopcion.objects.get(id=id)
        adopcionSerialized = AdopcionSerializer(adopcion)
        comentariosAdopcion = ComentarioAdopcion.objects.filter(adopcion=adopcion)
        comentariosSerialized = ComentarioAdopcionSerializer(comentariosAdopcion, many=True)
        data = {
            'success': {
                'adopcion': adopcionSerialized.data,
                'comentarios': comentariosSerialized.data 
            }
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def comentar_adopcion(request, id, username):
    if request.method == 'POST':
        comentario = request.POST['comentario']
        user = User.objects.get(username=username)
        usuario = Usuario.objects.get(user=user)
        adopcion = Adopcion.objects.get(id=id)
        new_comentario = ComentarioAdopcion.objects.create(adopcion=adopcion, usuario=usuario, comentario=comentario)
        new_comentario.save()
        data = {
            'success': {
                'todo_bien': 'todo_correcto'
            }
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def nueva_adopcion(request, username):
    if request.method == 'POST':
    	username = username
    	user = User.objects.get(username=username)
    	usuario = Usuario.objects.get(user=user)
    	descripcion = request.POST['descripcion']
    	foto = request.FILES['foto']
    	datos = {
    		'usuario': usuario.id,
    		'descripcion': descripcion,
    		'foto': foto
		}
    	serializerAdopcion = AdopcionSerializer(data=datos)
    	if serializerAdopcion.is_valid():
            adopcion = Adopcion.objects.create(usuario=usuario, descripcion=descripcion, foto=foto)
            adopcion.save()
            data = {
            	'success': {
            		'todo_bien': 'todo_correcto'
        		}
    		}
            return JSONResponse(data, status=200)
    	return JSONResponse(serializerAdopcion.errors, status=400)

@csrf_exempt
def nueva_adopcion_no_foto(request, username):
    if request.method == 'POST':
    	username = username
    	user = User.objects.get(username=username)
    	usuario = Usuario.objects.get(user=user)
    	descripcion = request.POST['descripcion']
    	adopcion = Adopcion.objects.create(usuario=usuario, descripcion=descripcion, foto=None)
    	adopcion.save()
    	if adopcion:
    		data = {
    			'success': {
    				'todo_bien': 'todo_correcto'
				}
			}
    		return JSONResponse(data, status=200)
    	else:
    		data = {
    			'error': {
    				'todo_mal': 'todo_incorrecto'
    			}
    		}
    		return JSONResponse(serializerAdopcion.errors, status=400)