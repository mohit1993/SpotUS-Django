from django import forms
from django.core.exceptions import ValidationError
from django.forms.extras.widgets import SelectDateWidget
from datetime import date

from eventhandler.models import Event
from accounts.models import UserAccount

class eventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = [
			'createdOn',
			'organiser',
			'eventSlug',
		]
		widgets = {
			'eventDate': SelectDateWidget(years = list(range(date.today().year,date.today().year + 2))),
		}

	def clean_eventDate(self):
		edate = self.cleaned_data['eventDate']
		if edate < date.today():
			raise ValidationError("Event date incorrect")
		return edate

	def clean_duration(self):
		x = self.cleaned_data['duration']
		try:
			if x < 1:
				raise ValidationError("Event must be of atleast 1 day")
			else:
				return x
		except: 
			raise ValidationError("Duration set incorrectly")

	def clean(self):
		cleaned_data = super(eventForm,self).clean()
		desc = cleaned_data.get('description')
		ven = cleaned_data.get('venue')
		name = cleaned_data.get('eventName')

		if not desc:
			raise forms.ValidationError("Description is required")
		
		if not ven:
			raise forms.ValidationError("Venue is required")
		
		if not name:
			raise forms.ValidationError("Event Name is required")

		return cleaned_data




