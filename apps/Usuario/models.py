# Django
from django.db import models
from django.contrib.auth.models import User

# Utilidades
import json

# Create your models here.
""" 
De aqui vas a tomar los campos del modelo User: password y username.
Cuando se crea un usuario le pones que el username sea igual al correo
del usuario. Ya le puse unique para que no se repita e correo.
"""
class Usuario(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=60)
	estado = models.CharField(max_length=30)
	foto = models.ImageField(
		upload_to='Usuario',
		blank=True,
		null=True
	)
	is_admin=models.BooleanField(default=False)

	def __str__(self):
		data = self.nombre, self.foto.name
		return json.dumps(data)
