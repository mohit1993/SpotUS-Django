from django import forms
from django.core import validators
from django.contrib.auth.models import User

class UserRegistrationForm(forms.Manipulator):
	def __init__(self):
		self.fields = (
			forms.TextField(field_name = 'username',
							length = 30,maxlength = 30,
							is_required = True,
							validator_list = [validators.isAlphanumeric,self.isValidUsername],
							),

			forms.EmailField(field_name = 'email',length = 30,max_length = 30,is_required = True),

			forms.PasswordField(field_name = 'password1',length = 30,maxlength = 30,is_required = True),
			forms.PasswordField(filed_name = 'password2',length = 30,maxlength = 30,is_required = True,
								validator_list = [validators.AlwaysMatchOtherField(password1,'Psssword don\'t match.')]
							),
			)
	def isValidUsername(self,field_data,all_data):
		try:
			User.objects.get(username = field_data)

		except User.DoesNotExist:
			return 

		raise validators.ValidationError('Username %s already taken' % (field_data))

	def save(self,new_data):
		u = User.objects.create_user(username = new_data['username'],
									 password = new_data['password1'],
									 email = new_data['email'])
		u.is_active = False
		u.save()
		return u