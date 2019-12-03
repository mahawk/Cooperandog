# Django
from django.utils.translation import ugettext_lazy as _
from django import forms

# Rest
from rest_framework import serializers

# Modelos
from django.contrib.auth.models import User
from apps.Usuario.models import Usuario

# Utilidades
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
    	password = data['password']
    	username = data['username']
    	if password in username:
    		raise serializers.ValidationError({
    			'passwordSim': _('¡La contraseña es similar al correo!.')	
			})
    	elif len(password) < 8: 
    		raise serializers.ValidationError({
    			'passwordShort': _('¡La contraseña es muy corta!.\n Debe contener al menos 7 caracteres.')	
    			})
    	else:
    		return data

    def validate_username(self, value):
    	regex = r'[a-z0-9._%+-]+@[a-z0-9.-]+[\\.][a-z]{2,}$'
    	if not re.match(regex, value):
    		raise serializers.ValidationError({
    			'correo': _('¡Ingrese un correo valido!.\n Ej: puppy@mail.com')	
		}) 
    	else:
    		return value

	# def validate_password(self, value):

class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usuario
		fields = ('nombre', 'estado', 'foto')

	def validate_foto(self, foto):
		if foto.name.endswith('.jpg') or foto.name.endswith('.jpeg') or foto.name.endswith('.png'):
			return foto
		else:
			raise serializers.ValidationError({
				'foto': _('¡Formato de archivo invalido!.\n Solo fotos con extencion .jpg, .jpeg o png.')
			})

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'