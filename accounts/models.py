from django.db import models
from django.contrib.auth.models import (AbstractBaseUser)
# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, is_active=True, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password(password)
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj
	def create_admin(self, email, password=None):
		user = self.create_user(
				email,
				password = password,
				is_admin = True
			)
		return user

class User(AbstractBaseUSer):
	email = models.EmailField(max_length = 255,Unique = True)
	active = models.BooleanField(default=True)
	admin = models.BooleanField(default = False)
	timestamp = models.DateTimeField(auto_now_add = True)

	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	objects = UserManager()

	@property
	def is_active(self):
		return self.active

	@property
	def is_admin(self):
		return self.admin

  