from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, name, email, password=None, is_staff = False, is_active = False, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('users must have a password')
        if not name:
            raise ValueError('users must have name')

        user = self.model(
            phone=phone,
            name = name,
            email = email
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using = self._db)
        return user
    
    def create_staffuser(self, phone, name, email, password=None):
        user = self.create_user(
            phone,
            name,
            email,
            password= password,
            is_staff= True,
            is_active=True
        )
        return user

    def create_superuser(self, phone, name, email, password=None):
        user = self.create_user(
            phone,
            name,
            email,
            password= password,
            is_staff= True,
            is_admin=True,
            is_active=True
        )
        return user
    



class User(AbstractBaseUser):
    phone_reg = RegexValidator( regex = r'^\d{10,13}$', message="Check number of digits")
    phone = models.CharField(validators=[phone_reg], max_length=14, unique=True)
    email = models.EmailField(default="")
    password=models.CharField(max_length=30, blank=False)
    name = models.CharField(max_length=255)
    first_login = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD= 'phone'
    REQUIRED_FIELDS=['name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.phone
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name

    def get_email_field_name(self):
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
    
    
    @property
    def is_active(self):
        return self.active