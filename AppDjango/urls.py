
from django.urls import path
from AppDjango import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:query>',views.profile, name='profile'),
    path('academy/', views.academy, name='academy'),
    path('event/', views.event, name='events'),
    path('form/', views.form, name='form'),
    path('academy/edit/<int:pk>/',  views.edit_academy, name='edit_academy'),
    path('profile/edit/', views.edit_user, name='edit_user'),
    path('profile/password/', views.change_password, name='change_password'),
]
