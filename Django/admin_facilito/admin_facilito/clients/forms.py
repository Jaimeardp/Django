from django import forms
from django.contrib.auth.models import User

"""
Constantes
"""

ERROR_MESSAGE_USER ={'required': 'El usuario es requerido','unique':'El nombre de usuario ya existe','invalid':'Ingrese un nombre valido'}
ERROR_MESSAGE_PASSWORD = {'required': 'La clave es requerido'}
ERROR_MESSAGE_EMAIL = {'required': 'El email es requerido','invalid':'Ingrese un correo valido'}

"""
Clases
"""

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password = forms.CharField(max_length = 20, widget = forms.PasswordInput())

#, widget = forms.PasswordInput()

class CreateUserForm(forms.ModelForm):
	username = forms.CharField(max_length = 20, error_messages=ERROR_MESSAGE_USER)
	password = forms.CharField(max_length = 20, widget = forms.PasswordInput(),error_messages= ERROR_MESSAGE_PASSWORD)
	email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)
	class Meta:
		model = User
		fields = ('username','password','email')

class EditUserForm(forms.ModelForm):
	username = forms.CharField(max_length = 20, error_messages=ERROR_MESSAGE_USER)
	email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)
	class Meta:
		model = User
		fields = ('username','email','first_name','last_name')
