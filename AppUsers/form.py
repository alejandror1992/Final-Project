from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
   # ModelForm
   password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
   password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

   class Meta:
       model = User
       fields = ['first_name', 'second_name', 'username', 'email', 'password1', 'password2']