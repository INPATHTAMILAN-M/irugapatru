from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from .managers import UserManager


gender_choices =(
    ("m", "Male"),
    ("f", "Female")
)





class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60, unique=True)    
    first_name = models.CharField(_('first name'), max_length=250)
    email = models.EmailField(_('email address'),unique=True,null=True )
    mobile_no = models.CharField(max_length=10,blank=True,null=True)   
    registered_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True) 
    is_staff=models.BooleanField(default=False)
    gender = models.CharField(choices = gender_choices, max_length=1,null=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.first_name:
            return self.first_name  
        else:
            return self.username      
     
        



    def get_full_name(self):
        if self.first_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        else:
            full_name = self.name
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)



'''class Instrument(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name'''
