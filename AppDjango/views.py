from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponseForbidden
from .form import EventForm, AcademyForm, ProfileForm
from .models import Academy, Event, UserProfile

def home (request):
    featured_academies = Academy.objects.filter(featured=True)
    featured_events = Event.objects.filter(featured=True)
    context = {"featured_academies":featured_academies,
               "featured_events": featured_events}
    return render(request, "home.html", context)

def academy (request):
    academy = Academy.objects.first()
    context = {"academy":academy,}
    return render(request, "academy.html",context)

def event (request):
    event = Event.objects.all()
    context = {"event":event,}
    return render(request, "events.html",context)

@login_required
def profile (request, query=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    academies = Academy.objects.all()
    events = Event.objects.all()
    if query:
      academies = academies.filter(name__icontains=query)
      events = events.filter(name__icontains=query)
    
    profile_form = ProfileForm()
    
    context = {
        'user_profile': user_profile,
        'academies': academies,
        'events': events,
        "profile_form":profile_form,
    }
    return render(request, "profile.html",context)

def form(request):
  if request.method == 'POST':
    event_form = EventForm(request.POST)
    academy_form = AcademyForm(request.POST)
    profile_form = ProfileForm(request.POST)
        
    if 'create_event' in request.POST:
       if request.user.is_authenticated and (request.user in academy.created_by.all() or request.user == request.user.profile.user):

          if event_form.is_valid():
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('events')
       else: return HttpResponseForbidden()

    elif 'create_profile' in request.POST:
      
      if profile_form.is_valid():
         profile = profile_form.save(commit=False)
         profile.user = request.user
         profile.save()
         return redirect('profile')
    
    elif 'create_academy' in request.POST:
      
      if academy_form.is_valid():
        academy = academy_form.save(commit=False)
        academy.created_by = request.user
        academy.save()
        return redirect('academy')
    
  else:
    event_form = EventForm()
    profile_form = ProfileForm()
    academy_form = AcademyForm()
        
  return render(request, 'form.html', {'EventForm': event_form, 'AcademyForm': academy_form, 'ProfileForm': profile_form})


@login_required
def edit_user(request):
    # Get the user's profile instance
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Initialize the profile form and associated forms
        profile_form = ProfileForm(request.POST, instance=user_profile)
        medal_form = ProfileForm.MedalForm(request.POST, instance=user_profile.medals)
        amateur_record_form = ProfileForm.RecordForm(request.POST, instance=user_profile.amateur_record)
        professional_record_form = ProfileForm.RecordForm(request.POST, instance=user_profile.professional_record)

        # Check if all forms are valid
        if profile_form.is_valid() and medal_form.is_valid() and amateur_record_form.is_valid() and professional_record_form.is_valid():
            # Save the forms
            profile = profile_form.save(commit=False)
            medal = medal_form.save()
            amateur_record = amateur_record_form.save()
            professional_record = professional_record_form.save()
            
            # Associate the forms with the profile
            profile.medals = medal
            profile.amateur_record = amateur_record
            profile.professional_record = professional_record
            
            # Save the profile
            profile.save()

            # Redirect to a success page or do something else
            return redirect('profile_success')  # Replace 'profile_success' with your success URL

    else:
        # If it's a GET request, initialize the forms with existing data
        profile_form = ProfileForm(instance=user_profile)
        medal_form = ProfileForm.MedalForm(instance=user_profile.medals)
        amateur_record_form = ProfileForm.RecordForm(instance=user_profile.amateur_record)
        professional_record_form = ProfileForm.RecordForm(instance=user_profile.professional_record)

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'medal_form': medal_form,
        'amateur_record_form': amateur_record_form,
        'professional_record_form': professional_record_form,
    })

@login_required
def edit_academy(request,academy_id):
   academy=get_object_or_404(Academy,id=academy_id)
   if request.user != academy.created_by:
      return HttpResponseForbidden("You don't have permission to edit this academy.")
   if request.method == "POST":
      form = AcademyForm(request.POST, instance=academy)
      if form.is_valid():
         form.save()
         return redirect("academy")
   else:
      form = AcademyForm(instance=academy)   
   return render(request, "edit_academy.html",{"form":form,"academy":academy})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'form.html', {'form': form})
