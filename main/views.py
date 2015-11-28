from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect, get_object_or_404
from main.models import Episode, EpisodeForm, Fiction, CommentForm
from django.core.urlresolvers import reverse

# Create your views here.
def home(request):
    if request.user.is_anonymous():
        return render(request, 'index.html',{'request':request})
    episodes = Episode.objects.filter(author=request.user.profile)
    fictions = [episode.fiction for episode in episodes]
    fictions = list(set(fictions))
    return render(request, 'index.html', {"fictions": fictions,'episodes':episodes,'request':request})

def notifications(request):
    return render(request, 'notifications.html', {})

def episode(request,episode_id):
    episode = Episode.objects.get(id=episode_id)
    stars = len(episode.stars.all())
    children = len(episode.children.all())
    commentForm = CommentForm()
    return render(request, 'episode/episode.html', {'episode':episode,'commentForm':commentForm, 'stars':stars,
                                                    'children': children,'request':request})

def comment_create(request,episode_id):
    comment = CommentForm(request.POST)
    episode =  get_object_or_404(Episode,pk=episode_id)
    if comment.is_valid():
        comment = comment.save(commit=False)
        comment.commenter = request.user.profile
        comment.episode = episode
        comment.save()
        return redirect(reverse("episode",kwargs={'episode_id':episode_id}))
    else:
        return render(request, 'episode/episode.html', {'episode':episode,'commentForm':comment})

def episode_create(request,fiction_id,parent_id):
    fiction = Fiction.objects.get(id=fiction_id)
    parent = Episode.objects.get(id=parent_id)
    if request.method == 'GET':
        form =  EpisodeForm()
        return render(request, 'episode/episode_create.html', {'form':form})
    else:
        form = EpisodeForm(request.POST)
        if form.is_valid():
            new_episode = form.save(commit=False)
            new_episode.fiction = fiction
            new_episode.parent = parent
            new_episode.author = request.user.profile
            new_episode.save()
            return redirect(reverse("episode",kwargs={'episode_id':new_episode.id}))
        else:
            return render(request, 'episode/episode_create.html', {
                'form': form
            })

def episode_edit(request,episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.user.profile.id != episode.author.id:
        return redirect(reverse("episode",kwargs={'episode_id':episode_id}))
    if request.method == 'GET':
        form = EpisodeForm(instance=episode)
        return render(request,'episode/episode_edit.html',{'form':form})
    else:
        form = EpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            form.save()
            return redirect(reverse("episode",kwargs={'episode_id':episode_id}))
        else:
            return render(request,'episode/episode_edit.html',{'form':form})


def star(request,episode_id):
    episode = get_object_or_404(Episode,pk=episode_id)
    episode.stars.add(request.user.profile)
    return redirect(reverse("episode",kwargs={'episode_id':episode_id}))

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

