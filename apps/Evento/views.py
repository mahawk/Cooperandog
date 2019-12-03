# Django
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Rest
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Modelos
from apps.Evento.models import Evento

# Serializer
from apps.Evento.serializers import EventoSerializer
from apps.Evento.serializers import EventosSerializer

# Create your views here.
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def eventos(request):
    if request.method == 'GET':
        eventos = Evento.objects.all()
        eventosSerialized = EventosSerializer(eventos, many=True)
        data = {
            'eventos': eventosSerialized.data
        }
        return JSONResponse(data, status=200)

@csrf_exempt
def evento_especifico(request, id):
    if request.method == 'GET':
        evento = Evento.objects.get(id=id)
        eventoSerialized = EventoSerializer(evento)
        data = {
            'success': {
                'evento': eventoSerialized.data,
            }
        }
        return JSONResponse(data, status=200)