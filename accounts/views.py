from django.shortcuts import render,render_to_response,get_object_or_404
from accounts.models import UserAccount,OrganiserAccount
from accounts.form import UserForm,OrganiserForm,UserLogin,OrganiserLogin
from django.views.generic import FormView,RedirectView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib import sessions
from django.http import Http404,HttpResponseRedirect
from django.http.response import HttpResponsePermanentRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,logout,authenticate
from django.forms import ValidationError

class LoginRequiredMixin(object):
	@classmethod
	def as_view(cls, **initkwargs):
		view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
		return login_required(view)

class UserRegistrationView(CreateView):
	model = UserAccount
	template_name = 'registration.html'
	form_class = UserForm
	group_name = 'normal_user'

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			url = request.GET.get("next")
			if url is None:
				url = '/'
			return HttpResponseRedirect(url)
		else:
			return super(UserRegistrationView,self).get(request,*args,**kwargs)

	def form_valid(self,form):
		self.object = form.save(commit = False)
		user = User.objects.create_user(
			username = form.cleaned_data['username'],
			password = form.cleaned_data['password'],
			)
		group = Group.objects.get(name = self.group_name)
		user.groups.add(group)
		self.object.user = user
		self.object.save()
		#return self.get_success_url()
		return super(UserRegistrationView,self).form_valid(form)

	def get_success_url(self):
		return reverse('user_profile',kwargs = {'pk':int(self.object.pk),'slug':self.object.nameSlug})

class OrganiserRegistrationView(CreateView):
	model = OrganiserAccount
	template_name = 'registration_organiser.html'
	form_class = OrganiserForm
	group_name = 'normal_organiser'
	
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			url = request.GET.get("next")
			if url is None:
				url = '/'
			return HttpResponseRedirect(url)
		else:
			return super(OrganiserRegistrationView,self).get(request,*args,**kwargs)

	def form_valid(self,form):
		self.object = form.save(commit = False)
		organiser = User.objects.create_user(
			username = form.cleaned_data['username'],
			password = form.cleaned_data['password'],
			)
		group = Group.objects.get(name = self.group_name)
		organiser.groups.add(group)
		self.object.organiser = organiser
		self.object.save()
		return super(OrganiserRegistrationView,self).form_valid(form)	

	def get_success_url(self):
		return reverse('organiser_profile',kwargs = {'pk':int(self.object.pk),'slug':self.object.nameSlug})


class UserProfileView(DetailView):
	model = UserAccount
	template_name = 'userprofile.html'
	queryset = UserAccount.objects.get_queryset()
	context_object_name = "obj"

	def get_object(self,*args,**kwargs):
		slug = self.kwargs.get(self.slug_url_kwarg,None)
		pk = self.kwargs.get('pk',None)

		data = UserAccount.objects.get(pk=pk)
		if data is not None:
			return data
		return super(UserProfileView,self).get_object(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		self.data = self.get_object()
		data_url = self.data.get_absolute_url()
		if self.request.path != data_url:
			return HttpResponsePermanentRedirect(data_url)
		return super(UserProfileView,self).get(request,*args,**kwargs)


class OrganiserProfileView(DetailView):
	model = OrganiserAccount
	template_name = 'organiserprofile.html'
	queryset = OrganiserAccount.objects.get_queryset()
	context_object_name = 'obj'

	def get_object(self,*args,**kwargs):
		slug = self.kwargs.get(self.slug_url_kwarg,None)
		pk = self.kwargs.get('pk',None)

		data = OrganiserAccount.objects.get(pk=pk)
		if data is not None:
			return data
		return super(OrganiserProfileView,self).get_object(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		self.data = self.get_object()
		data_url = self.data.get_absolute_url()
		if self.request.path != data_url:
			return HttpResponsePermanentRedirect(data_url)
		return super(OrganiserProfileView,self).get(request,*args,**kwargs)

class UserLoginView(FormView):
	
	form_class = UserLogin
	form_valid_message = "You're logged in now!"
	template_name = 'user_login.html'
	group_name = 'normal_user'
	success_url = '/'

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			url = request.GET.get("next")
			if url is None:
				url = '/'
			return HttpResponseRedirect(url)
		else:
			return super(UserLoginView,self).get(request,*args,**kwargs)

	def form_valid(self,form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']

		user = authenticate(username = username,password = password)

		self.success_url = self.request.GET.get('next',None)

		if self.success_url is None:
			self.success_url = '/'
		
		if user is not None and user.is_active:
			login(self.request,user)
			return super(UserLoginView,self).form_valid(form)

class OrganiserLoginView(FormView):

	form_class = OrganiserLogin
	form_valid_message = "You're logged in now!"
	template_name = 'organiser_login.html'
	group_name = 'normal_organiser'
	success_url = '/'

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			url = request.GET.get("next")
			if url is None:
				url = '/'
			return HttpResponseRedirect(url)
		else:
			return super(OrganiserLoginView,self).get(request,*args,**kwargs)

	def form_valid(self,form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']

		user = authenticate(username = username,password = password)

		self.success_url = self.request.GET.get('next',None)

		if self.success_url is None:
			self.success_url = '/'

		if user is not None and user.groups.filter(name = self.group_name).exists() == False:
			raise ValidationError("Sorry your credentials arent authorized to login as Organiser")

		elif user is not None and user.is_active:
			login(self.request,user)
			return super(OrganiserLoginView,self).form_valid(form)

		else:
			raise ValidationError("Account is either deactivated or not yet verified")


class LogoutView(RedirectView):
	#url = reverse('home')
	template_name = 'logout.html'
	url = '/'

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			logout(request)
		
		self.url = request.GET.get('next',None)

		if self.url is None:
			self.url= '/'

		return super(LogoutView,self).get(request,*args,**kwargs)


class UserRedirect(RedirectView):
	url = '/'
	def get(self,request,*args,**kwargs):
		pk = self.kwargs.get('pk',None)
		try:
			data = UserAccount.objects.get(pk=pk)
		except:
			raise ValidationError("Invalid Account accessed")
		self.url = data.get_absolute_url()
		return super(UserRedirect,self).get(request,*args,**kwargs)

class OrganiserRedirect(RedirectView):
	url = '/'
	def get(self,request,*args,**kwargs):
		pk = self.kwargs.get('pk',None)
		try:
			data = Organiser.objects.get(pk=pk)
		except:
			raise ValidationError("Invalid Account accessed")
		self.url = 'organiser/%(pk)s/%(slug)s/' % {'pk':pk,'slug':data.nameSlug}
		return super(UserRedirect,self).get(request,*args,**kwargs)