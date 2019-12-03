# Django
from django.utils.translation import ugettext_lazy as _

# Rest
from rest_framework import serializers

# Modelos
from apps.Adopciones.models import Adopcion
from apps.Adopciones.models import ComentarioAdopcion
from apps.Usuario.models import Usuario

class AdopcionSerializer(serializers.ModelSerializer):
	usuario = serializers.StringRelatedField()
	class Meta:
		model = Adopcion
		fields = ('usuario', 'descripcion', 'foto', 'fecha', 'hora')

	def validate_foto(self, foto):
		if foto.name.endswith('.jpg') or foto.name.endswith('.jpeg') or foto.name.endswith('.png'):
			return foto
		else:
			raise serializers.ValidationError({
                'foto': _('¡Formato de archivo invalido!.\n Solo fotos con extencion .jpg, .jpeg o png.')
            })

class ComentarioAdopcionSerializer(serializers.ModelSerializer):
	usuario = serializers.StringRelatedField()
	class Meta:
		model = ComentarioAdopcion
		fields = '__all__'

class AdopcionesSerializer(serializers.ModelSerializer):
	usuario = serializers.StringRelatedField()
	class Meta:
		model = Adopcion
		fields = ('id', 'usuario', 'descripcion', 'foto', 'fecha', 'hora')