# Django
from django.db import models

# Modelos
from apps.Usuario.models import Usuario

# Create your models here.
class Extravio(models.Model):
	usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
	anuncio = models.CharField(max_length=160)
	recompensa = models.FloatField()
	raza = models.CharField(max_length=60)
	color = models.CharField(max_length=40)
	fecha_extravio = models.DateField(auto_now_add=False)
	nombre = models.CharField(max_length=30)
	tamano = models.CharField(max_length=20)
	senas_particulares = models.TextField(max_length=360)
	lat = models.DecimalField(max_digits=20, decimal_places=16)
	lon = models.DecimalField(max_digits=20, decimal_places=16)
	descripcion = models.TextField(max_length=360)
	foto = models.ImageField(
		upload_to='Extravio',
		blank=True,
		null=True
	)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)

class ComentarioExtravio(models.Model):
	extravio = models.ForeignKey(Extravio, null=True, blank=True, on_delete=models.CASCADE)
	usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
	comentario = models.TextField(max_length=160)
	fecha = models.DateField(auto_now_add=True)
	hora = models.TimeField(auto_now_add=True)

