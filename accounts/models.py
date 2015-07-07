from django.db import models
import datetime
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from spotus import settings


genderChoices = (
				('M','Male'),
				('F','Female'),
				)

class PersonProfile(models.Model):
	
	class Meta:
		abstract = True

	firstName = models.CharField(max_length = 50,blank = False)
	lastName = models.CharField(max_length = 20)
	dateOfBirth = models.DateField(blank = False)
	dateOfJoining = models.DateField(default = timezone.now)
	gender = models.CharField(blank = False,max_length = 1,choices = genderChoices,default = 'M')
	profilePic = models.ImageField(upload_to = 'userprofile',blank = True)
	contactNumber = models.CharField(max_length = 15)
	address = models.TextField(max_length = 100)
	country = models.CharField(max_length = 15,blank = False)
	city = models.CharField(max_length = 40,blank = False)
	pincode = models.CharField(max_length = 10)
	nameSlug = models.SlugField(null = True)
	#activation_key = models.CharField(max_length = 48,blank = True)
	#key_expires = models.DateTimeField(blank = True)

	def save(self,*args,**kwargs):
		if self.pk is None:
			dateOfJoining = datetime.datetime.today()	
		return super(PersonProfile,self).save(*args,**kwargs)

class UserAccount(PersonProfile):
	email = models.EmailField(blank = True)
	user = models.OneToOneField(User)
			
	def get_absolute_url(self):
		return reverse('user_profile',kwargs = {'pk':int(self.pk),'slug':self.nameSlug})

	def save(self,*args,**kwargs):
		if self.pk is None:
			self.nameSlug = slugify(self.user.username)
		return super(UserAccount,self).save(*args,**kwargs)

class OrganiserAccount(PersonProfile):

	organiser = models.OneToOneField(User)
	companyName = models.CharField(max_length = 50)
	companyWebsite = models.CharField(max_length = 100)
	personalWebsite = models.CharField(max_length = 100)
	email = models.EmailField(blank = False)

	def save(self,*args,**kwargs):
		if self.pk is None:
			self.nameSlug = slugify(self.organiser.username)
		return super(OrganiserAccount,self).save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('organiser_profile',kwargs = {'pk':int(self.pk),'slug':self.nameSlug})







