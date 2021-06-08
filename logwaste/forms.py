from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import MyUser, Ewaste
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RFPAuthForm(AuthenticationForm):
    username = forms.CharField(error_messages={'required': 'This field is required'}, widget=TextInput(
        attrs={'class': 'bg'}))
    password = forms.CharField(error_messages={'required': 'This field is required'}, widget=PasswordInput(
        attrs={'class': 'bg'}))


class SignupForm(UserCreationForm):
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'bg'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'bg'}))

    class Meta:
        model = MyUser
        fields = ['full_name', 'email', 'mobile',
                  'address']
        labels = {'full_name': 'Name', 'email': 'Email',
                  'mobile': 'Mobile', 'address': 'Address'}
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'bg'}),
            'email': forms.EmailInput(attrs={'class': 'bg'}),
            'mobile': forms.TextInput(attrs={'class': 'bg'}),
            'address': forms.TextInput(attrs={'class': 'bg'}),
        }


class Ewastes(forms.ModelForm):
    class Meta:
        model = Ewaste
        fields = ['name', 'email', 'mobile', 'address',
                  'item_name', 'item_description', 'item_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg'}),
            'email': forms.EmailInput(attrs={'class': 'bg'}),
            'mobile': forms.TextInput(attrs={'class': 'bg'}),
            'address': forms.TextInput(attrs={'class': 'bg'}),
            'item_name': forms.TextInput(attrs={'class': 'bg'}),
            'item_description': forms.TextInput(attrs={'class': 'bg'}),
            'item_image': forms.ClearableFileInput(attrs={'class': 'bgi'})
        }
