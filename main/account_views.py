from django.contrib.auth import authenticate, login as do_login, logout as do_logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import ModelForm, EmailInput, PasswordInput
from django.shortcuts import render, redirect
from django.views.generic import View
from main.models import ProfilePhoto, Profile

def profile_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in and has an associated profile, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and hasattr(u, "profile"),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': EmailInput(attrs={
                'required': True
            }),
            'password': PasswordInput(attrs={
                'required': True
            }),
        }

class RegistrationView(View):
    def get(self, request):
        registerForm = RegisterForm()
        return render(request, 'sign_up.html', {'form': registerForm})

    def post(self, request):
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save()
            user.set_password(request.POST['password'])
            user.save()
            picture = ProfilePhoto.objects.create()
            Profile.objects.create(user=user, picture=picture)
            return redirect(reverse('login'))
        return render(request, 'sign_up.html', {'form': registerForm})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            do_login(request, user)
            return redirect(reverse('home'))
        else:
            return render(request, 'login.html', {'error': 'Authentication failed.', 'request': request})
    else:
        return render(request, 'login.html', {'request': request})

def logout(request):
    do_logout(request)
    return redirect(reverse('home'))