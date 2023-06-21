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

    styles=forms.ModelMultipleChoiceField(queryset=Style.objects.all(),widget=forms.CheckboxSelectMultiple, initial=Style.allowed_styles())

    class Meta:
        model = UserProfile
        fields = ['user',"bio","competitor", 'medals', 'amateur_record', 'professional_record', 'styles', 'academies_visited']
