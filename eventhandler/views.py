from django.shortcuts import render
from eventhandler.models import Event
from eventhandler.form import eventForm
from django.views.generic import RedirectView,ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import HttpResponsePermanentRedirect,HttpResponseRedirect


class NewEventRegister(CreateView):
	model = Event
	template_name = 'newevent.html'
	form_class = eventForm
	success_url = 'eventdetail'

	def get_success_url(self):
		return reverse('eventdetail',kwargs = {'pk':self.object.pk,'slug':self.object.eventSlug})

	def form_valid(self,form):
		self.object = form.save(commit = False)
		try:
			self.object.organiser = self.request.user.organiseraccount
		except:
			raise ValidationError("You must be logged in as organiser to create a new event")
		self.object.save()
		return super(NewEventRegister,self).form_valid(form)

class SingleEventView(DetailView):
	model = Event
	template_name = 'eventdetail.html'
	queryset = Event.objects.get_queryset()
	context_object_name = 'event'

	def get_object(self,*args,**kwargs):
		slug = self.kwargs.get(self.slug_url_kwarg,None)
		pk = self.kwargs.get('pk',None)

		eventdata = Event.objects.get(pk=pk)
		if eventdata is not None:
			return eventdata
		return super(SingleEventView,self).get_object(*args,**kwargs)	

	def get(self,*args,**kwargs):
		self.eventdata = self.get_object()
		event_url = self.eventdata.get_absolute_url()
		if self.request.path != event_url:
			return HttpResponsePermanentRedirect(event_url)
		return super(SingleEventView,self).get(*args,**kwargs)	


class SingleEventViewRedirect(RedirectView):
	queryset = Event.objects.get_queryset()
	
	def get(self,request,*args,**kwargs):
		pk = self.kwargs.get('pk',None)
		eventdata = Event.objects.get(pk=pk)
		self.url =  '/event/%(pk)s/%(slug)s/' % {'pk':pk,'slug':eventdata.eventSlug}
		return super(SingleEventViewRedirect,self).get(request,*args,**kwargs)


class EventsView(ListView):
	model = Event
	template_name = "eventsmainpage.html"
	context_object_name = "event_list"
	paginate_by = 3
