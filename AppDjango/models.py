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

class MedalManager(models.Manager):
    def get_queryset(self, allowed_styles):
        if allowed_styles == ['Karate', 'Judo', 'Taekwondo', 'KungFu']:
             return super().get_queryset().filter(style__name__in=self.allowed_styles)
        else:
            return Medal.object.none()

class Medal(models.Model):
    MEDAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze')
    ]
    medal = models.CharField(max_length=6, choices=MEDAL_CHOICES)
    count = models.IntegerField(default=0)
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='medals')
    
    objects = models.Manager()
    competitor_objects = MedalManager()

    def __str__(self):
        return f'{self.medal} medal({self.count}) for{self.style.name}'
    
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
    styles = models.ManyToManyField(Style, related_name='academies', limit_choices_to={"allowed_objects":True})
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    competitor = models.BooleanField(default=False)
    medals = models.ForeignKey(Medal, on_delete=models.CASCADE, null=True, blank=True)
    styles = models.ManyToManyField(Style, related_name='users')
    academies_visited = models.ManyToManyField(Academy, related_name='visitors')

    #FOR MMA:
    amateur_record = models.OneToOneField(Record, on_delete=models.CASCADE)
    professional_record = models.OneToOneField(Record, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.styles.filter(name='MMA').exists() and self.competitor is True:
            if not self.amateur_record:
                self.amateur_record = Record.objects.create()
            if not self.professional_record:
                self.professional_record = Record.objects.create()
        else:
            self.amateur_record = None
            self.professional_record = None

        super().save(*args, **kwargs)

    