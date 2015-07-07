from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.forms.extras.widgets import SelectDateWidget
import datetime

from accounts.models import UserAccount,OrganiserAccount
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex = r'^\+[0-9]{10,14}$',message = 'Contact number must be of format: +91xxxxxxxxxx. Example +919876543210')
pincode_regex = RegexValidator(regex = r'^[0-9]+$',message = 'Pincode must be a positive code')
username_regex = RegexValidator(regex = r'^[a-zA-Z]{1}[a-zA-Z0-9@_.]{4,}$',
	message = "Username should be of minimum length 5, begin with alphabet and must contain only letters,numbers and @_.")

password_regex = RegexValidator(regex = r'^[a-zA-Z]{1}[a-zA-Z0-9@_.]{5,}',
	message = "Password should be of minimum length 6, begin with alphabet and must contain only letters,numbers and @_.")

class LoginForm(forms.Form):

	username = forms.CharField(max_length = 30,widget = forms.TextInput(),validators = [username_regex])
	password = forms.CharField(max_length = 20,widget = forms.PasswordInput(),validators = [password_regex])
	groupname = ''
	
	def clean_password(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		print username
		try:
			user = User.objects.get(username = username)
			if self.groupname == 'normal_user':
				user.useraccount
			
			elif self.groupname == 'normal_organiser':
				user.organiseraccount
		
		except AttributeError:
			raise ValidationError("No account with this username exists")

		if user.check_password(password) is False:
			raise ValidationError("Invalid username or password entered")

		if user.is_active is False:
			raise ValidationError("Account is deactivated or not verified")
		
		return password

class UserLogin(LoginForm):
	groupname = 'normal_user'

class OrganiserLogin(LoginForm):
	groupname = 'normal_organiser'


class UserForm(forms.ModelForm):
	class Meta:
		model = UserAccount
		fields = [
					'firstName',
					'lastName',
					'address',
					'city',
					'country',
					'pincode',
					'contactNumber',
					'dateOfBirth',
					'gender',
					'profilePic',
					'email'
				]
		contactNumber = forms.CharField(validators = [phone_regex])
		pincode = forms.CharField(validators = [pincode_regex])
		widgets = {
			'dateOfBirth': SelectDateWidget(years = list(reversed(range(1950,datetime.date.today().year))))
		}

	username = forms.CharField(max_length = 30,widget = forms.TextInput(),validators = [username_regex])
	password = forms.CharField(max_length = 20,widget = forms.PasswordInput,validators = [password_regex])
	confirmPassword = forms.CharField(max_length = 20,widget = forms.PasswordInput,validators = [password_regex])

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username = username)
			raise ValidationError("username %s already taken" % (username))
		except User.DoesNotExist:
			print "HELLO"
			return username

	def clean_confirmPassword(self):
		password = self.cleaned_data['password']
		confirmPassword = self.cleaned_data['confirmPassword']
		print password,confirmPassword
		if password and confirmPassword and password == confirmPassword:
			return password
		else:
			raise ValidationError("Passwords must match")

	def clean_contactNumber(self):
		number = self.cleaned_data['contactNumber']
		if number is '':
			return number
		try:
			if UserAccount.objects.get(contactNumber = number):
				raise ValidationError("Account with this phone number is already registered")
		except ObjectDoesNotExist:
			return number

	def clean_email(self):
		e = self.cleaned_data['email']
		if e is '':
			return e
		try:
			if UserAccount.objects.get(email = e):
				raise ValidationError("Account with this email is already registered")
		except ObjectDoesNotExist:
			return e

	def clean(self):
		cleaned_data = super(UserForm,self).clean()
		return cleaned_data

class OrganiserForm(forms.ModelForm):
	class Meta:
		model = OrganiserAccount
		fields = [
					'firstName',
					'lastName',
					'address',
					'city',
					'country',
					'pincode',
					'contactNumber',
					'dateOfBirth',
					'gender',
					'profilePic',
					'companyName',
					'companyWebsite',
					'personalWebsite',
					'email',
				]
		contactNumber = forms.CharField(validators = [phone_regex])
		pincode = forms.CharField(validators = [pincode_regex])
		widgets = {
			'password': forms.PasswordInput(),
			'dateOfBirth': SelectDateWidget(years = list(reversed(range(1950,datetime.date.today().year))))
		}

	username = forms.CharField(max_length = 30,widget = forms.TextInput(),validators = [username_regex])
	password = forms.CharField(max_length = 20,widget = forms.PasswordInput,validators = [password_regex])
	confirmPassword = forms.CharField(max_length = 20,widget = forms.PasswordInput,validators = [password_regex])

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username = username)
			raise ValidationError("username %s already taken" % (username))
		except ObjectDoesNotExist:
			return username

	def clean_confirmPassword(self):
		pass1 = self.cleaned_data['password']
		pass2 = self.cleaned_data['confirmPassword']

		if pass1 and pass2 and pass1 == pass2:
			return pass1
		raise ValidationError("Passwords must match")

	def clean_contactNumber(self):
		number = self.cleaned_data['contactNumber']
		if number is '':
			return number
		try:
			if OrganiserAccount.objects.get(contactNumber = number):
				raise ValidationError("Account with this phone number is already registered")
		except ObjectDoesNotExist:
			return number

	def clean_email(self):
		e = self.cleaned_data['email']
		if e is '':
			raise ValidationError("You must provide an email address")
		try:
			if OrganiserAccount.objects.get(email = e):
				raise ValidationError("Account with this email is already registered")
		except ObjectDoesNotExist:
			return e

	def clean_personalWebsite(self):
		pweb = self.cleaned_data['personalWebsite']
		if pweb is '':
			return pweb
		try:
			if OrganiserAccount.objects.get(personalWebsite = pweb):
				raise ValidationError("Account with this personal website is already registered")
		except ObjectDoesNotExist:
			return pweb

	def clean(self):
		cleaned_data = super(OrganiserForm,self).clean()
		return cleaned_data
