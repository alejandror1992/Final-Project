from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from AppUsers.form import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate

def register(request):
   if request.method == "POST":
       registerform = UserRegisterForm(request.POST)

       if registerform.is_valid():
           registerform.save()
           url_ok = reverse('Home')
           return redirect(url_ok)
   else:  # GET
       registerform = UserRegisterForm()
   return render(
       request=request,
       template_name='AppUsers/register.html',
       context={'form': registerform},
   )

def login_view(request):
   if request.method == "POST":
       form = AuthenticationForm(request, data=request.POST)

       if form.is_valid():
           data = form.cleaned_data
           user = data.get('username')
           password = data.get('password')
           user = authenticate(username=user, password=password)
           # user can be a user or None
           if user:
               login(request=request, user=user)
               url_ok = reverse('Home')
               return redirect(url_ok)
   else:  # GET
       form = AuthenticationForm()
   return render(
       request=request,
       template_name='AppUsers/login.html',
       context={'form': form},
   )

class CustomLogoutView(LogoutView):
    template_name = 'AppUsers/logout.html'
