# Django
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Modelos
from apps.Usuario.models import Usuario

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class FormUsuario(forms.ModelForm):
	class Meta:
		model = Usuario

		fields = (
			'nombre',
			'estado',
		)

		labels = {
			'nombre': 'Nombre',
			'estado': 'Estado'
		}

	def clean_nombre(self, *args, **kwargs):
		nombre = self.cleaned_data.get("nombre")
		if "Edgar" not in nombre:
			raise forms.ValidationError('nombre': "El nombre debe contener Edgar")
		else:
			return nombre

    # def save(self, commit=True):
    #     user = super(UserCreateForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user