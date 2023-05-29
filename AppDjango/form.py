from django import forms
from .models import Event, Academy, UserProfile, Style

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'description']

class AcademyForm(forms.ModelForm):
    styles = forms.ModelMultipleChoiceField(queryset=Style.allowed_objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Academy
        fields = ['name', 'address', 'description', 'created_by', 'featured']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['styles'].initial = self.instance.styles.values_list('pk', flat=True)

    def save(self, commit=True):
        academy = super().save(commit=False)
        if commit:
            academy.save()
        if academy.pk:
            academy.styles.set(self.cleaned_data['styles'])
            self.save_m2m()
        return academy

class ProfileForm(forms.ModelForm):
    styles = forms.ModelMultipleChoiceField(queryset=Style.allowed_objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'medals', 'amateur_record', 'professional_record', 'styles', 'academies_visited']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['styles'].initial = self.instance.styles.values_list('pk', flat=True)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        if profile.pk:
            profile.styles.set(self.cleaned_data['styles'])
            self.save_m2m()
        return profile
