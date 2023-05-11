
from django.urls import path
from AppDjango import views

urlpatterns = [
    path('Home/', views.home, name='Home'),
    path('Academy/', views.academy, name='Academy'),
    path('Event/', views.events, name='Events'),
    path('Form/', views.form, name='Form'),
    path('Academy/edit/<int:pk>/',  views.edit_academy, name='edit_academy'),
    path('profile/edit/', views.edit_user, name='edit_user'),
    path('profile/password/', views.change_password, name='change_password'),
]
