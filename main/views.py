import os
import urllib.parse
from django.conf import settings as django_settings
from django.forms import ModelForm, ChoiceField, Select
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from haystack.query import SearchQuerySet
from main.account_views import profile_required
from main.models import Comment, Fiction, Episode, Profile, Genre
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
    evolve_count = len(episode.children.all())
    commentForm = CommentForm()
    starred = request.user.profile in episode.stars.all() if hasattr(request.user,"profile") else False
    previous = episode.previous()
    next = episode.next()
    return render(request, 'episode/episode.html',
                  {'episode': episode, 'previous_list': previous, 'next_list': next, 'starred': starred,
                   'evolve_count': evolve_count, 'commentForm': commentForm})

@profile_required
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

BEFORE_AFTER_CHOICE = (
    ('1', 'After'),
    ('0', 'Before'),
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
        self.fields['after'].label = 'Where does this episode come sequentially? (99% of the time it will be "After")'

@profile_required
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
            new_episode.sentiment = new_episode.calculate_sentiment()
            new_episode.save()
            return redirect(reverse("episode", kwargs={'episode_id': new_episode.id}))
        else:
            return render(request, 'episode/episode_create.html', {
                'form': form, 'request': request
            })

@profile_required
def episode_edit(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.user.profile.id != episode.author.id:
        return redirect(reverse("episode", kwargs={'episode_id': episode_id}))
    if request.method == 'GET':
        form = EpisodeForm(instance=episode)
        is_root = False
        if episode.fiction.root.id == episode.id:
           is_root = True
        return render(request, 'episode/episode_edit.html', {'form': form, 'is_root': is_root})
    else:
        form = EpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            episode = form.save(commit=False)
            episode.sentiment = episode.calculate_sentiment()
            episode.save()
            return redirect(reverse("episode", kwargs={'episode_id': episode_id}))
        else:
            return render(request, 'episode/episode_edit.html', {'form': form, 'request': request})

@profile_required
def episode_disown(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.user.profile.id == episode.author.id:    
        ghost = Profile.objects.get(pk=1)
        episode.author = ghost
        episode.save()
    return redirect(reverse("episode", kwargs={'episode_id': episode_id}))

@profile_required
def star(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    profile = request.user.profile
    if request.user.profile in episode.stars.all():
        episode.unstar(profile)
    else:
        episode.star(profile)
    episode.save()
    return redirect(reverse("episode", kwargs={'episode_id': episode_id}))

def explore(request):
    fictions = dict()
    genres = Genre.objects.all()
    for genre in genres:
        fics = list(Fiction.objects.filter(genre=genre))
        fictions[genre] = sorted(fics, key=lambda x: x.popularity(), reverse=True)
    return render(request, 'explore.html', {'fictions': fictions, 'genres': genres})

def fiction(request, fiction_id):
    fiction = get_object_or_404(Fiction, pk=fiction_id)
    return render(request, 'fiction.html', {'fiction': fiction, 'fiction_id': fiction_id})

from fpdf import FPDF, HTMLMixin

class HTMLPDF(FPDF, HTMLMixin):
    pass

def generate_pdf(current_episode, episodes):
    pdf = HTMLPDF()
    pdf.add_page()
    fiction_html = ("<h1 align='center'>" + current_episode.fiction.title + "</h1>").encode('utf8').decode('latin1')
    pdf.write_html(fiction_html)
    author_html = ("<p align='right'>Originally Started By " + current_episode.fiction.starter.display_name + "</p>").encode('utf8').decode('latin1')
    pdf.write_html(author_html)
    for episode in episodes:
        title_html  = ("<h2>" + episode.title + "</h2>").encode('utf8').decode('latin1')
        pdf.write_html(title_html)
        pdf.write_html(episode.content.encode('utf8').decode('latin1'))
        pdf.write_html("<br />")
    pdf_name = urllib.parse.quote(current_episode.fiction.title) + '_' + ''.join([str(episode.id) for episode in episodes])
    pdf.output(os.path.join(django_settings.MEDIA_ROOT, 'fictions', pdf_name + '.pdf'), 'F')
    return pdf_name

def storyline(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    fiction = episode.fiction
    episodes = [episode]
    previous_episode_list = episode.previous()
    while previous_episode_list:
        episode = previous_episode_list[0]
        episodes.insert(0, episode)
        previous_episode_list = episode.previous()
    pdf_name = generate_pdf(episode, episodes)
    return render(request, 'storyline.html', {'episodes': episodes, 'fiction': fiction, 'pdf_name': pdf_name})

def pdf(request, pdf_name):
    with open(os.path.join(django_settings.MEDIA_ROOT, 'fictions', pdf_name + '.pdf'), 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=' + pdf_name + '.pdf'
        return response
    pdf.closed

class FictionCreate(CreateView):
    model = Fiction
    fields = ["genre", "title", "created_date"]
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        self.object = form.save(commit=False)
        self.object.starter = profile
        self.object.save()
        root = Episode(fiction=self.object, title="Edit Me", summary="Add your summary here", author=profile)
        root.save()
        fiction = Fiction.objects.get(pk=self.object.pk)
        fiction.root = root
        fiction.save()
        return HttpResponseRedirect(self.get_success_url())

from django.db.models import Q
def search_query(request):
    query = request.GET['query']
    query_set = SearchQuerySet().filter(Q(content=query))
    return render(request, "search/search.html", {"word": query, "qs": query_set})
