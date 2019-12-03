# Django
from django.db import models

# Modelos
from apps.Usuario.models import Usuario

# Create your models here.
class Adopcion(models.Model):
	usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
	descripcion = models.TextField(max_length=360)
	foto = models.ImageField(
		upload_to='Adopciones',
		blank = True,
		null = True
	)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)

class ComentarioAdopcion(models.Model):
	adopcion = models.ForeignKey(Adopcion, null=True, blank=True, on_delete=models.CASCADE)
	usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
	comentario = models.TextField(max_length=160)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)