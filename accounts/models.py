from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, email, username=None, password=None, is_active=True,is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(
			email = self.normalize_email(email),
			username=username
		)
		user_obj.set_password(password)
		user_obj.admin = is_admin
		user_obj.is_active = is_active
		user_obj.staff = is_staff
		user_obj.save(using=self._db)
		return user_obj

	#creates the super user
	def create_superuser(self, email,username=None, password=None):
		user = self.create_user(
				email,
				username = username,
				password = password,
				is_admin = True,
				is_staff = True
			)
		return user
	#creates the staff user
	def create_staffuser(self, email, username=None, password=None):
		user = self.create_user(
				email,
				username = username,
				password = password,
				is_staff = True
			)
		return user

class User(AbstractBaseUser):
	email = models.EmailField(max_length = 255,unique = True)
	username = models.CharField(max_length = 255, blank = True, unique = True, null=True)
	is_active = models.BooleanField(default=True)
	admin = models.BooleanField(default = False)
	staff = models.BooleanField(default = False)
	timestamp = models.DateTimeField(auto_now_add = True)


	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_username(self):
		if self.username:
			return self.username
		return self.email

	def get_email(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True 

	def has_module_perms(self, app_label):
		return True


	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

		

  