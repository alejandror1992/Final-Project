from django.db import models
from django.contrib.auth.models import User
from AppUsers.form import AvatarForm

class AllowedStylesManager(models.Manager):
    def get_queryset(self):
        allowed_styles = Style.allowed_styles()
        return super().get_queryset().filter(name__in=allowed_styles)

class Style(models.Model):
    name = models.CharField(max_length=100)
    allowed_styles = AllowedStylesManager()  # custom manager
    @classmethod
    def allowed_styles(cls):
        return ['Karate', 'Judo', 'Taekwondo','MMA', 'KungFu']  # replace with your allowed styles
    def __str__(self):
        return self.name

class MedalManager(models.Manager):
    def get_queryset(self):
        allowed_styles = Style.allowed_styles()
        if UserProfile.objects.filter(competitor=True).exists():
             return super().get_queryset().filter(style__name__in= allowed_styles)
        else:
            return Medal.objects.none()

class Medal(models.Model):
    MEDAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze')
    ]
    gold = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)
    bronce = models.IntegerField(default=0)
    style = models.ManyToManyField(Style, related_name='medals')
    
    objects = models.Manager()
    competitor_objects = MedalManager()

    def __str__(self):
        return f'Medals - Gold:{self.gold}, Silver:{self.silver}, Bronce:{self.bronce}'
    
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
    competitor = models.BooleanField(default=False)
    medals = models.ForeignKey(Medal, on_delete=models.CASCADE, null=True, blank=True)
    styles = models.ManyToManyField(Style, related_name='users',default=Style.allowed_styles)
    academies_visited = models.ManyToManyField(Academy, related_name='visitors')

    #FOR MMA:
    amateur_record = models.OneToOneField("Record", on_delete=models.CASCADE, related_name="amateur_profile", null=True, blank=True)
    professional_record = models.OneToOneField("Record", on_delete=models.CASCADE, related_name="professional_profile", null=True, blank=True)

    def __str__(self):
        medals_info = f"Medals:\n---------\nGold: {self.medals.gold}\nSilver: {self.medals.silver}\nBronze: {self.medals.bronze}"
        amateur_record_info = f"Amateur record:\n---------\n{self.amateur_record}"
        professional_record_info = f"Professional record:\n---------\n{self.professional_record}"
        styles_info = f"Styles:\n---------\n" + ", ".join(str(style) for style in self.styles.all())
        academies_visited_info = f"Academies visited:\n---------\n" + ", ".join(str(academy) for academy in self.academies_visited.all())
        return f"Competitor: {self.user.username}\n\n{medals_info}\n\n{amateur_record_info}\n\n{professional_record_info}\n\n{styles_info}\n\n{academies_visited_info}"

    def save(self, *args, **kwargs):
      if self.competitor:
        if self.styles.filter(name='MMA').exists():
            if not hasattr(self, "amateur_record"):
                self.amateur_record = Record.objects.create()
            if not hasattr(self, "professional_record"):
                self.professional_record = Record.objects.create()
            else:
                if not self.medals:
                    self.medals =Medal.objects.create()
        else:
            self.medals = None
            self.amateur_record = None
            self.professional_record = None

        super().save(*args, **kwargs)

    