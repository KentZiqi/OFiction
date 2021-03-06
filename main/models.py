from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, null=True)
    display_name = models.CharField(blank=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    subscriptions = models.ManyToManyField("Fiction", related_name="subscribers", blank=True)
    picture = models.OneToOneField("ProfilePhoto", null=True)

    def __str__(self):
        return self.display_name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ProfilePhoto(models.Model):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.file.size
        if file_size > 4096 * 4096:
            raise ValidationError("Max file size is 4MB")

    image = models.ImageField(upload_to='photo/', height_field='height',
                              width_field='width', validators=[validate_image],
                              default='default_profile.png')
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbs/', blank=True, null=True)
    date = models.DateTimeField(default=datetime.datetime.now)

    # Adapted from http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
    def create_thumbnail(self):

        if not self.image:
            return

        from io import BytesIO
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (500, 500)

        from mimetypes import MimeTypes

        mime = MimeTypes()
        mime_type = mime.guess_type(self.image.url)

        DJANGO_TYPE = mime_type
        if DJANGO_TYPE[0] == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE[0] == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        else:
            return

        self.image.open()
        r = BytesIO(self.image.read())
        fullsize_image = Image.open(r)
        image = fullsize_image.copy()

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
        self.thumbnail.save('{}_thumbnail.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self, **kwargs):
        self.create_thumbnail()
        force_update = False
        if self.id:
            force_update = True
        super(ProfilePhoto, self).save(force_update=force_update)

    def __str__(self):
        return self.image.url

class Fiction(models.Model):
    genre = models.ForeignKey(Genre, related_name='fictions')

    title = models.CharField(max_length=200)
    starter = models.ForeignKey(Profile)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    root = models.ForeignKey("main.Episode", related_name="start", null=True)

    def __str__(self):
        return self.title + " by " + str(self.starter)

    def popularity(self):
        popularity = 0
        episodes = Episode.objects.filter(fiction=self)
        for episode in episodes:
            popularity += episode.popularity
        return popularity

class Episode(models.Model):
    fiction = models.ForeignKey(Fiction)

    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)
    after = models.BooleanField(default=True)
    duplicate = models.ForeignKey("self", related_name="duplicates", null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Profile)
    content = RichTextField(default="This episode is empty")
    stars = models.ManyToManyField(Profile, related_name="favorites")
    created_date = models.DateTimeField(default=datetime.datetime.now)
    summary = models.CharField(blank=True, null=True, max_length=1000)
    popularity = models.IntegerField(default=0)
    sentiment = models.DecimalField(decimal_places=5, max_digits=6, default=0)

    def previous_ids_without_parent(self):
        previous_list = list(self.children.filter(after=False))
        return [previous.id for previous in previous_list]

    def previous(self):
        previous = list(self.children.filter(after=False))
        if self.after and self.parent:
            previous.append(self.parent)
        previous.sort(key=lambda episode: episode.popularity, reverse=True)
        return previous

    def next_ids_without_parent(self):
        next_list = list(self.children.filter(after=True))
        return [next.id for next in next_list]

    def next(self):
        next = list(self.children.filter(after=True))
        if not self.after and self.parent:
            next.append(self.parent)
        next.sort(key=lambda episode: episode.popularity, reverse=True)
        return next

    def getID(self):
        episodes = self.fiction.episode_set.all()
        return list(episodes).index(self) + 1

    def star(self, profile):
        self.stars.add(profile)
        self.popularity = len(self.stars.all())

    def unstar(self, profile):
        self.stars.remove(profile)
        self.popularity = len(self.stars.all())

    def calculate_sentiment(self):
        import requests
        from bs4 import BeautifulSoup
        url = 'http://text-processing.com/api/sentiment/'
        summary_and_content_as_text = self.summary + BeautifulSoup(self.content).text;
        response = requests.post(url, data= {"text": summary_and_content_as_text})
        if response.status_code == 200:
            json = response.json()
            positive = json['probability']['pos']
            negative = json['probability']['neg']
            score = positive - negative
            return score
        else:
            return 0 # Default to neutral

    def __str__(self):
        return "#" + str(self.getID()) + ": " + self.fiction.title + "/" + self.title

class Comment(models.Model):
    commenter = models.ForeignKey(Profile)
    episode = models.ForeignKey(Episode)
    body = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.body + " by " + self.commenter
