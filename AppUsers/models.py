from django.db import models
from django.contrib.auth.models import User

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="avatars", null=True, blank=True )

    def __str__(self):
        return f"Profile Picture:"