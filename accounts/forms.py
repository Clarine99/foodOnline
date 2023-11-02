from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, UserProfile
from .validators import allow_only_images_validator
class UserForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
        print('INI DI FORMSS')
    
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        print('ini conf pass', confirm_password)
        if password != confirm_password:
            raise forms.ValidationError('password does not match')
        
class UserProfileForm(forms.ModelForm):
    profile_pic = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}),validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}),validators=[allow_only_images_validator])
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'start typing...', 'required':'required'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    
    class Meta:
        model = UserProfile
        fields = ['profile_pic','cover_photo','address','country','state','city','pin_code','longitude','latitude',]
    
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            if field == 'longitude' or field == 'latitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'



