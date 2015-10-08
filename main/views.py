from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def notifications(request):
    return render(request, 'notifications.html', {})

def episode(request):
    return render(request, 'episode.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def explore(request):
    return render(request, 'explore.html', {})

def storyline(request):
    return render(request, 'storyline.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def sign_in(request):
    return render(request, 'sign_in.html', {})

def sign_up(request):
    return render(request, 'sign_up.html', {})

def welcome(request):
    return render(request, 'welcome.html', {})