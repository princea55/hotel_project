from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupUser(UserCreationForm):
    contact = forms.CharField(widget=forms.NumberInput, max_length=10)
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2','contact']


class LoginUser(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
        