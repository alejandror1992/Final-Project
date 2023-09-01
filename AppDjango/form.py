from django import forms
from .models import Event, Academy, UserProfile, Style, Record, Medal

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'description']

class AcademyForm(forms.ModelForm):

    class Meta:
        model = Academy
        fields = ['name', 'address', 'description', 'created_by', 'featured']


class ProfileForm(forms.ModelForm):
    class Meta:
        styles = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=Style.allowed_styles(),)
        model = UserProfile
        fields = ['user', 'bio', 'competitor', 'academies_visited']

    class MedalForm(forms.ModelForm):
        class Meta:
            model = Medal
            fields = ['gold', 'silver', 'bronze']

    class RecordForm(forms.ModelForm):
        class Meta:
            model = Record
            fields = ['wins', 'losses', 'no_contest']
