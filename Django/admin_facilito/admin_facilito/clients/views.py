# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect

#from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required

#Formularios
from forms import LoginForm
from forms import CreateUserForm
from forms import EditUserForm
from forms import EditPasswordForm

from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView


from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
# Create your views here.
class ShowView(DetailView):
	model = User
	template_name = 'show.html'
	slug_field= 'username' # Que campo de la bd
	slug_url_kwarg ='username_url' #Que atributo de la bd

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

class DashboardView(LoginRequiredMixin,View):
	login_url = 'client:login'

	def get(self,request,*args,**kwargs):
		return render(request,'dashboard.html',{})

@login_required(login_url='client:login')
def logout(request):
	logout_django(request)
	return redirect('client:login')

class Create(CreateView):
	success_url = reverse_lazy('client:login')	
	template_name = 'create.html'
	model = User
	#fields = ('username','email')
	form_class = CreateUserForm

	def form_valid(self,form):
		self.object = form.save(commit = False) 
		self.object.set_password(self.object.password)
		self.object.save()
		return HttpResponseRedirect(self.get_success_url()) 

class Edit(UpdateView):
	model = User
	template_name = 'edit.html'
	success_url = reverse_lazy('client:dashboard')
	form_class = EditUserForm

	def get_object(self,queryset=None):
		return self.request.user

def edit_password(request):
	form = EditPasswordForm(request.POST or None)
	if form.is_valid():
		print ("Formulario Valido")
	context = {'form':form}
	return render(request,'edit_password.html',context)
		


