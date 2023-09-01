from django.db import models
from django.contrib.auth.models import User
from AppUsers.form import AvatarForm

class Style(models.Model):
    KARATE="Karate"
    JUDO = "Judo"
    MMA = "MMA"
    def allowed_styles():
        return [(KARATE,'Karate'), (JUDO,'Judo'), (MMA,'MMA'),]  # replace with your allowed styles
    name = models.CharField(max_length=20, choices= allowed_styles)
    
    def __str__(self):
        return self.name

class Medal(models.Model):

    gold = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)
    bronze = models.IntegerField(default=0)

    def __str__(self):
        return f"Medals:\n---------\nGold: {self.gold}\nSilver: {self.silver}\nBronze: {self.bronze}"
    
class Record(models.Model):
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    no_contest = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.wins} - {self.losses} - {self.no_contest}'

class Academy(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField()
    styles = models.ManyToManyField(Style, related_name='academies')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academies_created')
    featured = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    featured = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    @property
    def allowed_styles(self):
        return Style.allowed_styles()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = AvatarForm
    bio = models.TextField(blank=True)
    styles = models.ManyToManyField(Style, blank=True)
    competitor = models.BooleanField(default=False)
    medals = models.OneToOneField(Medal, on_delete=models.CASCADE, null=True, blank=True)
    academies_visited = models.ManyToManyField(Academy, related_name='visitors')
    #FOR MMA:
    amateur_record = models.ForeignKey(Record, on_delete=models.CASCADE, null=True, blank=True, related_name="amateur_record")
    professional_record = models.ForeignKey(Record, on_delete=models.CASCADE, null=True, blank=True, related_name="profesional_record")

    def save(self, *args, **kwargs):
      if self.competitor:
        if self.styles.filter(name='MMA').exists():
            if not hasattr(self, "amateur_record"):
                self.amateur_record = Record.objects.create()
                self.amateur_record.save()
                self.amateur_record.styles.set(self.styles.all())
            if not hasattr(self, "professional_record"):
                self.professional_record = Record.objects.create()
                self.professional_record.save()
                self.professional_record.styles.set(self.styles.all())
            else:
                if not self.medals:
                    self.medals =Medal.objects.create()
                    self.medals.save()
                    self.medals.styles.set(self.styles.all())
        else:
            self.medals = None
            self.amateur_record = None
            self.professional_record = None

        super().save(*args, **kwargs)
