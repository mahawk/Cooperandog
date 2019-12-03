# Django
from django.utils.translation import ugettext_lazy as _
from django import forms

# Rest
from rest_framework import serializers

# Modelos
from apps.Evento.models import Evento

# Serializers
class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ('nombre', 'fecha', 'hora_inicio', 'hora_final', 'lugar', 'descripcion',
                  'foto')

class EventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ('id','nombre', 'fecha', 'hora_inicio', 'hora_final', 'lugar', 'descripcion',
                  'foto')