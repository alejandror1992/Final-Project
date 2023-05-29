from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
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
    user_profile = UserProfile.objects.get(user=request.user) 
    academies = Academy.objects.all()
    events = Event.objects.all()
    if query:
      academies = academies.filter(name__icontains=query)
      events = events.filter(name__icontains=query)
    
    context = {
        'user_profile': user_profile,
        'academies': academies,
        'events': events,
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
         profile.user = request.user.profile.user
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
        
  return render(request, 'AppDjango/form.html', {'EventForm': event_form, 'AcademyForm': academy_form, 'ProfileForm': profile_form})


@login_required
def edit_academy(request, pk):
    academy = Academy.objects.get(created_by=request.user, pk=pk)
    if request.method == 'POST':
        if not academy:
           return HttpResponseForbidden()
        form = AcademyForm(request.POST, instance=academy)
        if form.is_valid():
           form.save()
           return redirect('academy')
    else:
        form = AcademyForm(instance=academy)
    return render(request, 'AppDjango/form.html', {'form': form})


@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user.profile)
    return render(request, 'AppDjango/form.html', {'form': form})

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
    return render(request, 'AppDjango/form.html', {'form': form})
