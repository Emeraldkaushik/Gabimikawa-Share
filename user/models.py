from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils import timezone

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser =True
		user.role = 'admin'
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)
# class UserManager(BaseUserManager):
#     def create_user(self, username ,password, **extra_fields):
#         if not username:
#             raise ValueError("Users must have an username")
#         if not password:
#             raise ValueError("Users must enter password")
#         user = self.model(
#             username=username,
#             **extra_fields
#             )
#         user.set_password(password)
#         user.is_active = True
#         user.role = "admin"

#         user.type = check
#         user.save(using=self._db)
#         return user
	
#     def create_staffuser(self, username, password):
#         user = self.create_user(username,password=password)
#         user.is_staff = True
#         user.is_active = True
#         user.role = "admin"


#         user.type = check
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password):
#         user = self.create_user(
#             password=password,
#             username=username
#             )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.is_active = True
#         user.role = "admin"

#         user.type = check
#         user.save(using=self._db)
#         return user


   

class User(AbstractBaseUser,PermissionsMixin):
	# username = models.CharField(max_length=500,blank=True, unique=True)
	email = models.EmailField(_('email address'), unique=True)

	full_name = models.CharField(max_length=300,null=True)
	
	last_login = models.DateTimeField(verbose_name='last_login', auto_now_add=True)
	mobile= models.CharField(_('Mobile Number'),null=True,max_length=12)

	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	# type = models.ForeignKey(ClientType,on_delete=models.CASCADE)
	# percentage = models.IntegerField(default=0,null=True,blank=True)
	password = models.CharField(max_length=100,blank=True,null=True)

	address = models.CharField(max_length=100,blank=True,null=True)
	street = models.CharField(max_length=100,blank=True,null=True)
	landmark =models.CharField(max_length=100,blank=True,null=True)
	pincode =models.CharField(max_length=100,blank=True,null=True)
	
	# company_type = models.ManyToManyField(CompanyType)


	update_at = models.DateTimeField(auto_now=True)
	create_at = models.DateTimeField(auto_now_add=True)

	
	objects = UserManager()
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []
	
	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
	

	def __str__(self):
		return str(self.full_name)


class GetInTouch(models.Model):
	name = models.CharField(max_length=200,null=True,blank=True)
	email = models.CharField(max_length=200,null=True,blank=True)
	mobile = models.CharField(max_length=200,null=True,blank=True)
	message = models.CharField(max_length=200,null=1000,blank=True)
	update_at = models.DateTimeField(auto_now=True)
	create_at = models.DateTimeField(auto_now_add=True)
