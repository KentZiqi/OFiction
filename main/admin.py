from django.contrib import admin
from main.models import Episode, Section, Profile, Fiction

# Register your models here.
admin.site.register(Episode);
admin.site.register(Section);
admin.site.register(Profile);
admin.site.register(Fiction)