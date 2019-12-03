# Django
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Rest
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Modelos
from django.contrib.auth.models import User
from apps.Usuario.models import Usuario
from apps.Extravio.models import Extravio
from apps.Extravio.models import ComentarioExtravio

# Serializer
from apps.Extravio.serializers import ExtravioSerializer
from apps.Extravio.serializers import ExtraviosSerializer
from apps.Extravio.serializers import ComentarioExtravioSerializer

# Funciones
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def extravios(request):
    if request.method == 'GET':
        extravios = Extravio.objects.all()
        extravioSerialized = ExtraviosSerializer(extravios, many=True)
        data = {
            'extravios': extravioSerialized.data
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def numero_comentarios(request):
    if request.method == 'GET':
        extravios = Extravio.objects.all()
        cantidadCom = []
        for extravio in extravios:
            comentarioExtravio = ComentarioExtravio.objects.filter(extravio=extravio)
            comentariosSerialized = ComentarioExtravioSerializer(comentarioExtravio, many=True)
            cantidadCom.append(len(comentariosSerialized.data))
        data = {
            'comentarios': cantidadCom
        }
        return JSONResponse(data, status=200)


@csrf_exempt
def extravio_especifico(request, id):
    if request.method == 'GET':
        extravio = Extravio.objects.get(id=id)
        extravioSerialized = ExtravioSerializer(extravio)
        comentariosExtravio = ComentarioExtravio.objects.filter(extravio=extravio)
        comentariosSerialized = ComentarioExtravioSerializer(comentariosExtravio, many=True)
        data = {
            'success': {
                'extravio': extravioSerialized.data,
                'comentarios': comentariosSerialized.data 
            }
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def comentar_extravio(request, id, username):
    if request.method == 'POST':
        comentario = request.POST['comentario']
        user = User.objects.get(username=username)
        usuario = Usuario.objects.get(user=user)
        extravio = Extravio.objects.get(id=id)
        new_comentario = ComentarioExtravio.objects.create(extravio=extravio, usuario=usuario, comentario=comentario)
        new_comentario.save()
        data = {
            'success': {
                'todo_bien': 'todo_correcto'
            }
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def nuevo_extravio(request, username):
    if request.method == 'POST':
        username = username
        user = User.objects.get(username=username)
        usuario = Usuario.objects.get(user=user)
        anuncio = request.POST['anuncio']
        recompensa = request.POST['recompensa']
        raza = request.POST['raza']
        color = request.POST['color']
        fecha = request.POST['fechaExtravio']
        nombre = request.POST['nombre']
        tamanio = request.POST['tamanio']
        senas = request.POST['senasPart']
        lat = request.POST['latitud']
        lon = request.POST['longitud']
        descripcion = request.POST['descripcion']
        foto = request.FILES['foto']
        datos = {
            'usuario': usuario.id,
            'anuncio': anuncio,
            'recompensa': recompensa,
            'raza': raza,
            'color': color,
            'fecha_extravio': fecha,
            'nombre': nombre,
            'tamano': tamanio,
            'senas_particulares': senas,
            'lat': lat,
            'lon': lon,
            'descripcion': descripcion,
            'foto': foto
        }
        serializerExtravio = ExtravioSerializer(data=datos)
        if serializerExtravio.is_valid():
            extravio = Extravio.objects.create(usuario=usuario, anuncio=anuncio, recompensa=recompensa, raza=raza,
                    color=color, fecha_extravio=fecha, nombre=nombre, tamano=tamanio, senas_particulares=senas,
                    lat=lat, lon=lon, descripcion=descripcion, foto=foto)
            extravio.save()
            data = {
                'success': {
                    'todo_bien': 'todo_correcto'
                }
            }
            return JSONResponse(data, status=200)
        return JSONResponse(serializerExtravio.errors, status=400)

@csrf_exempt
def comentarExtravio(request):
    if request.method == 'POST':
        comen = request.POST['comentario']
        publicacion = request.POST['publicacion']
        usuario = request.POST['usuario']
        u = Usuario.objects.get(id = usuario)
        p = Extravio.objects.get(id = publicacion)
        if ComentarioExtravio.objects.create(usuario = u, extravio = p, comentario = comen):
            data = {
                'todo_bien': 'todo_correcto'
            }
            return JSONResponse(data, status=200)
        else:
            data = {
                'todo_mal': 'todo_malo'
            }
            return JSONResponse(data, status=400)

def publicacionExtravio(request):
    if request.method == 'POST':
        publicacion = Extravio.objects.get(id = request.POST['publicacion'])
        publicacion['comentarios'] = ComentarioExtravio.objects.filter(extravio__id = publicacion['id']).values('comentario','usuario__nombre')
        return JSONResponse(publicacion, status=200)