# Django
from django.db import models

# Modelos
from apps.Usuario.models import Usuario

# Create your models here.
class Rescate(models.Model):
	usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
	descripcion = models.TextField(max_length=160)
	foto = models.ImageField(
		upload_to='Rescate',
		blank=True,
		null=True
	)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)

	class Meta:
		ordering = ('-fecha',)

class ComentarioRescate(models.Model):
	rescate = models.ForeignKey(Rescate, null=True, blank=True, on_delete=models.CASCADE)
	usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
	comentario = models.TextField(max_length=160)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)

		


