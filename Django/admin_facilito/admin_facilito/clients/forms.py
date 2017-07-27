from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password = forms.CharField(max_length = 20, widget = forms.PasswordInput())

#, widget = forms.PasswordInput()

class CreateUserForm(forms.ModelForm):
	username = forms.CharField(max_length = 20, 
		error_messages={'required': 'El usuario es requerido','unique':'El nombre de usuario ya existe'
		,'invalid':'Ingrese un nombre valido'})
	password = forms.CharField(max_length = 20, widget = forms.PasswordInput(),
		error_messages={'required': 'La clave es requerido'})
	email = forms.CharField(error_messages={'required': 'El email es requerido','invalid':'Ingrese un correo valido'})
	class Meta:
		model = User
		fields = ('username','password','email')
