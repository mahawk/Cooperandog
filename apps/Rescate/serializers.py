# Django
from django.utils.translation import ugettext_lazy as _

# Rest
from rest_framework import serializers

# Modelos
from apps.Rescate.models import Rescate
from apps.Rescate.models import ComentarioRescate
from apps.Usuario.models import Usuario

class RescateSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = Rescate
        fields = ('usuario', 'descripcion', 'foto', 'fecha', 'hora')

    def validate_foto(self, foto):
        if foto.name.endswith('.jpg') or foto.name.endswith('.jpeg') or foto.name.endswith('.png'):
            return foto
        else:
            raise serializers.ValidationError({
                'foto': _('¡Formato de archivo invalido!.\n Solo fotos con extencion .jpg, .jpeg o png.')
            })

class ComentarioRescateSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = ComentarioRescate
        fields = '__all__'

class RescatesSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = Rescate
        fields = ('id','usuario','descripcion','foto', 'fecha', 'hora')