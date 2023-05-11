from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AllowedStylesManager(models.Manager):
    def get_queryset(self):
        allowed_styles = ['Karate', 'Judo', 'Taekwondo','MMA', 'KungFu']  # replace with your allowed styles
        return super().get_queryset().filter(name__in=allowed_styles)

class Style(models.Model):
    name = models.CharField(max_length=100)

    objects = models.Manager()  # default manager
    allowed_objects = AllowedStylesManager()  # custom manager

    def __str__(self):
        return self.name

class Academy(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField()
    styles = models.ManyToManyField(Style, related_name='academies', limit_choices_to={"allowed_objects":True})
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academies_created')

    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    styles = models.ManyToManyField(Style, related_name='users')
    academies_visited = models.ManyToManyField(Academy, related_name='visitors')

    def __str__(self):
        return self.user.username

    