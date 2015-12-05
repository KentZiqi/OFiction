from django.forms import ModelForm, ChoiceField, Select
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Comment, Fiction, Episode, Profile
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import CreateView

def home(request):
    if not hasattr(request.user, "profile"):
        return render(request, 'index.html', {'request': request})
    episodes = Episode.objects.filter(author=request.user.profile)
    fictions = [episode.fiction for episode in episodes]
    fictions = list(set(fictions))
    return render(request, 'index.html', {"fictions": fictions, 'episodes': episodes})

def notifications(request):
    return render(request, 'notifications.html', {})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

def episode(request, episode_id):
    episode = Episode.objects.get(id=episode_id)
    children = len(episode.children.all())
    commentForm = CommentForm()
    starred = request.user.profile in episode.stars.all()
    return render(request, 'episode/episode.html', {'episode': episode, 'starred': starred, 'commentForm': commentForm, 'children': children, 'request': request})

def comment_create(request, episode_id):
    comment = CommentForm(request.POST)
    episode = get_object_or_404(Episode, pk=episode_id)
    if comment.is_valid():
        comment = comment.save(commit=False)
        comment.commenter = request.user.profile
        comment.episode = episode
        comment.save()
        return redirect(reverse("episode", kwargs={'episode_id': episode_id}))
    else:
        return render(request, 'episode/episode.html', {'episode': episode, 'commentForm': comment, 'request': request})

BEFORE_AFTER_CHOICE =(
    ('0', 'Before'),
    ('1', 'After'),
)
class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = ['title', 'summary', 'content', 'after']
        widgets = {
            'after': Select(choices=BEFORE_AFTER_CHOICE),
        }

    def __init__(self, *args, **kwargs):
        super(EpisodeForm, self).__init__(*args, **kwargs)
        self.fields['after'].label = 'Where does this episode come sequentially?'

def episode_create(request, fiction_id, parent_id):
    fiction = Fiction.objects.get(id=fiction_id)
    parent = Episode.objects.get(id=parent_id)
    if request.method == 'GET':
        form = EpisodeForm(initial={'after': '1'})
        return render(request, 'episode/episode_create.html', {'form': form, 'request': request})
    else:
        form = EpisodeForm(request.POST)
        if form.is_valid():
            new_episode = form.save(commit=False)
            new_episode.fiction = fiction
            new_episode.parent = parent
            new_episode.author = request.user.profile
            new_episode.save()
            return redirect(reverse("episode", kwargs={'episode_id': new_episode.id}))
        else:
            return render(request, 'episode/episode_create.html', {
                'form': form, 'request': request
            })

def episode_edit(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.user.profile.id != episode.author.id:
        return redirect(reverse("episode", kwargs={'episode_id': episode_id}))
    if request.method == 'GET':
        form = EpisodeForm(instance=episode, initial={'after':'1'})
        return render(request, 'episode/episode_edit.html', {'form': form, 'request': request})
    else:
        form = EpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            form.save()
            return redirect(reverse("episode", kwargs={'episode_id': episode_id}))
        else:
            return render(request, 'episode/episode_edit.html', {'form': form, 'request': request})

def star(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    profile = request.user.profile
    if request.user.profile in episode.stars.all():
        episode.unstar(profile)
    else:
        episode.star(profile)
    episode.save()
    return redirect(reverse("episode", kwargs={'episode_id': episode_id}))

def next(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    children = episode.children.order_by('-popularity')
    return render(request,'episode/next.html',{'children':children})

def explore(request):
    return render(request, 'explore.html', {})

def storyline(request):
    return render(request, 'storyline.html', {})

def settings(request):
    return render(request, 'settings.html', {})

class FictionCreate(CreateView):
    model = Fiction
    fields = ["genre", "title", "starters", "created_date"]
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        self.object = form.save()
        root = Episode(fiction=self.object, title="Hello World", author=profile)
        root.save()
        fiction = Fiction.objects.get(pk=self.object.pk)
        fiction.root = root
        fiction.save()
        return HttpResponseRedirect(self.get_success_url())