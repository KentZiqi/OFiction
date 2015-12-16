from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from main.models import Profile, ProfilePhoto, User

def profile(request,profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile_preview = profile.picture.thumbnail.url
    return render(request, 'profile.html', {"user": profile, "preview_url": profile_preview})

class ProfilePhotoForm(ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ["image"]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "description"]

class ProfileEditView(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        photo_form = ProfilePhotoForm(instance=profile.picture)
        profile_form = ProfileForm(instance=profile)
        profile_preview = profile.picture.thumbnail.url
        return render(request, "edit_profile.html",
                      {"preview_url": profile_preview, "photo_form": photo_form, "profile_form": profile_form})

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        photo_form = ProfilePhotoForm(instance=profile.picture)
        profile_form = ProfileForm(instance=profile)
        if 'picture' in self.request.POST:
            photo_form = ProfilePhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                image = photo_form.cleaned_data['image']
                profile = Profile.objects.get(user=request.user)
                ProfilePhoto.objects.update_or_create(profile=profile, defaults={'image': image})
        elif 'profile' in self.request.POST:
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
        profile_preview = profile.picture.thumbnail.url
        return render(request, "edit_profile.html",
                      {"preview_url": profile_preview, "photo_form": photo_form, "profile_form": profile_form})