from django.db import models
import datetime
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.core.urlresolvers import reverse
from django.utils import timezone

from accounts.models import OrganiserAccount

class Event(models.Model):
	class Meta:
		unique_together = ("eventName","eventDate","venue")
	eventName = models.CharField(max_length = 30,blank = False)
	eventCaption = models.CharField(max_length = 100,blank = True)
	eventPoster = models.ImageField(upload_to = 'poster',blank = True)
	createdOn = models.DateTimeField(default = timezone.now)
	eventDate = models.DateField(blank = False,null = False,default = timezone.now)
	duration = models.PositiveSmallIntegerField(blank = False,null = False,default = 0)
	organiser = models.ForeignKey(OrganiserAccount)
	venue = models.CharField(max_length = 20,blank = False,default = '')
	description = models.TextField(max_length = 1000,blank = False,default = '')
	eventSlug = models.SlugField(null = True,blank = True)

	def save(self,*args,**kwargs):
		if self.pk is None:
			self.createdOn = datetime.datetime.today()
		self.eventSlug = slugify(unidecode(self.eventName))
		super(Event,self).save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('eventdetail',kwargs = {'pk':int(self.pk),'slug':self.eventSlug})