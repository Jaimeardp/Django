# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect

#from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required

from forms import LoginForm
from forms import CreateUserForm

from django.views.generic import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class ShowView(DetailView):
	model = User
	template_name = 'show.html'
	slug_field= 'username'

#def show(request):
#	return HttpResponse("Hola desde el cliente")

class LoginView(View):
	form = LoginForm()
	message = None
	template = 'login.html'

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			return redirect('client:dashboard')
		return render(request,self.template,self.get_context())

	def post(self,request,*args,**kwargs):
		username_post = request.POST['username']
		password_post = request.POST['password']
		user = authenticate(username=username_post,password= password_post) # Recibe la contraseña en texto plano
		# Luego luego lo encripta y lo compara con la pass que esta en la DB
		print user
		if user is not None:
			login_django(request,user)
			return redirect('client:dashboard')
		else:
			self.message="Usuario o Pass incorrecto"
		return render(request,self.template,self.get_context())

	def get_context(self):
		return {'form':self.form,'message':self.message}

def login_(request):
	if request.user.is_authenticated():
		return redirect('client:dashboard')
	message = None
	#TEMPLATE
	#nombre = 'Jaime'
	#edad = '21'
	#context ={'nombre_usu': nombre,'edad':edad}
	#return render(request,'login.html',context)
	#FORMULARIO
	if request.method == 'POST':
		username_post = request.POST['username']
		password_post = request.POST['password']
	
		user = authenticate(username=username_post,password= password_post) # Recibe la contraseña en texto plano
		# Luego luego lo encripta y lo compara con la pass que esta en la DB
		print user
		if user is not None:
			login_django(request,user)
			return redirect('client:dashboard')
		else:
			message="Usuario o Pass incorrecto"

	form = LoginForm()
	context ={
		'form' : form,
		'message': message,
	}
	return render(request,'login.html',context)

class DashboardView(LoginRequiredMixin,View):
	login_url = 'client:login'

	def get(self,request,*args,**kwargs):
		return render(request,'dashboard.html',{})

@login_required(login_url='client:login') #DEcoradores : Verifica si el usuario esta logeado, caso contrario te dirige a login
def dashboard(request):
	return render(request,'dashboard.html',{})

@login_required(login_url='client:login')
def logout(request):
	logout_django(request)
	return redirect('client:login')

def create(request):
	form = CreateUserForm(request.POST or None)
	if request.method == 'POST':
		if(form.is_valid()):
			user = form.save(commit = False) # Nos regresa un objecto usermodel y guarda a la DB
			user.set_password(user.password) # Metodo de nuestro user, que encripta
			# user.password que es de nuestro formulario 
			user.save() # De esta manera ya estoy almacenando en la DB encriptada
			return redirect('client:login')
	context = {
		'form':form
	}
	return render(request,'create.html',context)