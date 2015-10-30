from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def home(request):
    fictions = Fiction.objects.all()
    return render(request, 'index.html', {"fictions": fictions})

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

from django.views.generic.edit import CreateView
from main.models import Fiction, Episode, Profile

class FictionCreate(CreateView):
    model = Fiction
    fields = ["section", "title", "starters", "created_date"]
    template_name_suffix = "_create_form"
    success_url = "/"

    def form_valid(self, form):
       self.object = form.save()
       root = Episode(fiction=self.object, title="Hello World", author=Profile.objects.first())
       root.save()
       fiction = Fiction.objects.get(pk=self.object.pk)
       fiction.root = root
       fiction.save()
       return HttpResponseRedirect(self.get_success_url())

