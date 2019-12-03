# Django
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Modelos
from django.contrib.auth.models import User
from apps.Rescate.models import Rescate
from apps.Rescate.models import ComentarioRescate
from apps.Usuario.models import Usuario


# Rest
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Serializer
from apps.Rescate.serializers import RescateSerializer
from apps.Rescate.serializers import ComentarioRescateSerializer
from apps.Rescate.serializers import RescatesSerializer
# Funciones

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def rescates(request):
	if request.method == 'GET':
		rescates = Rescate.objects.all()
		rescatesSerialized = RescatesSerializer(rescates, many=True)
		data = {
			'rescates': rescatesSerialized.data,
		}
		return JSONResponse(data, status=200)

@csrf_exempt
def numero_comentarios(request):
    if request.method == 'GET':
        rescates = Rescate.objects.all()
        cantidadCom = []
        for rescate in rescates:
            comentariosRescate = ComentarioRescate.objects.filter(rescate=rescate) 
            comentariosSerialized = ComentarioRescateSerializer(comentariosRescate, many=True)
            cantidadCom.append(len(comentariosSerialized.data))
        data = {
            'comentarios': cantidadCom
        }
        return JSONResponse(data, status=200)


@csrf_exempt
def rescate_especifico(request, id):
    if request.method == 'GET':
        rescate = Rescate.objects.get(id=id)
        rescateSerialized = RescateSerializer(rescate)
        comentariosRescate = ComentarioRescate.objects.filter(rescate=rescate)
        comentariosSerialized = ComentarioRescateSerializer(comentariosRescate, many=True)
        data = {
            'success': {
                'rescate': rescateSerialized.data,
                'comentarios': comentariosSerialized.data 
            }
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def comentar_rescate(request, id, username):
    if request.method == 'POST':
        comentario = request.POST['comentario']
        user = User.objects.get(username=username)
        usuario = Usuario.objects.get(user=user)
        rescate = Rescate.objects.get(id=id)
        new_comentario = ComentarioRescate.objects.create(rescate=rescate, usuario=usuario, comentario=comentario)
        new_comentario.save()
        data = {
            'success': {
                'todo_bien': 'todo_correcto'
            }
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def nuevo_rescate(request, username):
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
    	serializerRescate = RescateSerializer(data=datos)
    	if serializerRescate.is_valid():
            rescate = Rescate.objects.create(usuario=usuario, descripcion=descripcion, foto=foto)
            rescate.save()
            data = {
            	'success': {
            		'todo_bien': 'todo_correcto'
        		}
    		}
            return JSONResponse(data, status=200)
    	return JSONResponse(serializerRescate.errors, status=400)

# @csrf_exempt
# def nuevo_rescate_no_foto(request, username):
#     if request.method == 'POST':
#     	username = username
#     	user = User.objects.get(username=username)
#     	usuario = Usuario.objects.get(user=user)
#     	descripcion = request.POST['descripcion']
#     	rescate = Rescate.objects.create(usuario=usuario, descripcion=descripcion, foto=None)
#     	rescate.save()
#     	if rescate:
#     		data = {
#     			'success': {
#     				'todo_bien': 'todo_correcto'
# 				}
# 			}
#     		return JSONResponse(data, status=200)
#     	else:
#     		data = {
#     			'error': {
#     				'todo_mal': 'todo_incorrecto'
#     			}
#     		}
#     		return JSONResponse(data, status=400)

# @csrf_exempt
# def nuevo_rescate(request):
#     if request.method == 'POST':
#         u = request.POST['usuario']
#         descripcion = request.POST['descripcion']
#         foto = request.Files['imagen']
#         usu = Usuario.objects.get(id = u)
#         datos = {
#             'usuario': usu,
#             'descripcion': descripcion,
#             'foto': foto
#         }

#         serializerRescate = RescateSeri(data = datos)

#         if serializerRescate.is_valid():
#             extra = Rescate.objects.create(usuario = usu, descripcion = descripcion, foto = foto)
#             extra.save()
#             data = {
#                 'todo_bien': 'todo_correcto'
#             }
#             return JSONResponse(data, status=200)
#         return JSONResponse(serializerRescate.errors, status=400)

# def rescates(request):
#     if request.method == 'POST':
#         todos_rescates = Rescate.objects.all()
#         serializerRescate = RescatesSeri(data = todos_rescates, many = True)
#         if serializerRescate.is_valid():
#             return JSONResponse(serializerRescate.data, status=200)

# def comentarRescate(request):
#     if request.method == 'POST':
#         comen = request.POST['comentario']
#         publicacion = request.POST['publicacion']
#         usuario = request.POST['usuario']
#         u = Usuario.objects.get(id = usuario)
#         p = Rescate.objects.get(id = publicacion)
#         if ComentarioRescate.objects.create(usuario = u, adopcion = p, comentario = comen):
#             data = {
#                 'todo_bien': 'todo_correcto'
#             }
#             return JSONResponse(data, status=200)
#         else:
#             data = {
#                 'todo_mal': 'todo_malo'
#             }
#             return JSONResponse(data, status=400)

# def publicacionRescate(request):
#     if request.method == 'POST':
#         publicacion = Rescate.objects.get(id = request.POST['publicacion'])
#         publicacion['comentarios'] = ComentarioRescate.objects.filter(adopcion__id = publicacion['id']).values('comentario','usuario__nombre')
#         return JSONResponse(publicacion, status=200)
