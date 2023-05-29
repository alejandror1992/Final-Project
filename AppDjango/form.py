from django import forms
from .models import Event, Academy, UserProfile, Style

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'description']

class AcademyForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['styles'].queryset = Style.allowed_objects.all()
    class Meta:
        model = Academy
        fields = ['name', 'address', 'description', 'styles', 'created_by', 'featured']

class ProfileForm(forms.ModelForm):
    styles = forms.ModelMultipleChoiceField(queryset= Style.objects.all())
    class Meta:
        model = UserProfile
        fields = ['user','bio', 'medals', 'amateur_record', 'professional_record', 'styles', 'academies_visited']