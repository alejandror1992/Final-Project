from django.contrib import admin
from django.urls import path
from AppUsers.views import register, login_view, CustomLogoutView

urlpatterns = [ 
path ('register/', register, name='register'),
path ('login/', login_view, name='login'),
path ('logout/', CustomLogoutView.as_view(), name='logout'),
 ]