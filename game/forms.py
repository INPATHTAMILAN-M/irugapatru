from django import forms
from django.forms import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.safestring import mark_safe
from string import Template
from django.contrib.auth.models import Group
from PIL import Image
from django.db.models import Q
from django.core.exceptions import ValidationError




class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Mail Id','class' : 'reg_form_input_1 input email-input'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password','class' : 'reg_form_input_1 input password-input'}))
    

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Custom error, if you not verified kindly verify it'
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email Address"


class Signup_Form(UserCreationForm): 
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(Signup_Form, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
 

