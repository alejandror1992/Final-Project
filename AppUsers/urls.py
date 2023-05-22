from django.urls import path
from AppUsers.views import register, login_view, CustomLogoutView

path ('register/', register, name='register'),
path ('login/', login_view, name='login'),
path ('logout/', CustomLogoutView, name='logout'),