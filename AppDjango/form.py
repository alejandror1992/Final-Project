from django import forms
from .models import Event, Academy, UserProfile, Style, Record, Medal

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'description']

class AcademyForm(forms.ModelForm):
    styles = forms.ModelMultipleChoiceField(queryset=Style.objects.all(), widget=forms.CheckboxSelectMultiple)

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
    styles = forms.ModelMultipleChoiceField(queryset=Style.objects.all(), widget=forms.CheckboxSelectMultiple)
    academies_visited = forms.ModelMultipleChoiceField(queryset=Academy.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio','competitor', 'medals', 'amateur_record', 'professional_record']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['styles'].initial = self.instance.styles.values_list('pk', flat=True)
            self.fields['academies_visited'].initial = self.instance.academies_visited.values_list('pk', flat=True)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        if profile.pk:
            profile.styles.set(self.cleaned_data['styles'])
            profile.academies_visited.set(self.cleaned_data["academies_visited"])
            self.save_m2m()

            allowed_styles = Style.allowed_styles()
            
            if any("MMA" in allowed_styles for style in profile.styles.values_list('name', flat=True)):
              if profile.competitor:
                if not profile.amateur_record:
                    profile.amateur_record = Record.objects.create()
                if not profile.professional_record:
                    profile.professional_record = Record.objects.create()
              else:
                profile.amateur_record = None
                profile.professional_record = None

            if any(style in ['Karate', 'Judo'] for style in profile.styles.values_list('name', flat=True)):
                if not profile.medals:
                    profile.medals = Medal.objects.create(style=Style.objects.get(name='Karate'))
        return profile
