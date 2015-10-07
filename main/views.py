from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def notifications(request):
    return render(request, 'notifications.html', {})

def work(request):
    return render(request, 'work.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def explore(request):
    return render(request, 'explore.html', {})

def storyline(request):
    return render(request, 'storyline.html', {})

def settings(request):
    return render(request, 'settings.html', {})