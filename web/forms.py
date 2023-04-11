from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from api.models import Posts

class PostForm(forms.ModelForm):

    class Meta:
        model=Posts
        fields="__all__"

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()        
