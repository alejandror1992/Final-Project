from django import forms
from .models import Event, Academy, UserProfile, Style

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'description']

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ['name', 'address', 'description', 'styles']

class ProfileForm(forms.ModelForm):
    styles = forms.ModelMultipleChoiceField(queryset= Style.objects.all())
    class Meta:
        model = UserProfile
        fields = ['user','bio', 'styles', 'academies_visited']