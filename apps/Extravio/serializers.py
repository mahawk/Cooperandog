# Django
from django.utils.translation import ugettext_lazy as _
from django import forms

# Rest
from rest_framework import serializers

# Modelos
from apps.Extravio.models import Extravio
from apps.Extravio.models import ComentarioExtravio
from apps.Usuario.models import Usuario

class ExtravioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = Extravio
        fields = ('usuario', 'anuncio', 'recompensa', 'raza', 'color', 'fecha_extravio',
                  'nombre', 'tamano', 'senas_particulares', 'lat', 'lon', 'descripcion',
                  'foto', 'fecha', 'hora')

    def validate_foto(self, foto):
        if foto.name.endswith('.jpg') or foto.name.endswith('.jpeg') or foto.name.endswith('.png'):
            return foto
        else:
            raise serializers.ValidationError({
                'foto': _('¡Formato de archivo invalido!.\n Solo fotos con extencion .jpg, .jpeg o png.')
            })

class ExtraviosSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = Extravio
        fields = ('id', 'usuario','anuncio', 'recompensa', 'raza', 'color', 'fecha_extravio',
                  'nombre', 'tamano', 'senas_particulares', 'lat', 'lon', 'descripcion', 
                  'foto', 'fecha', 'hora')

class ComentarioExtravioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = ComentarioExtravio
        fields = '__all__'