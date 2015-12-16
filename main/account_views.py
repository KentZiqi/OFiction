from django.forms import *
from django.contrib.auth import authenticate, login as do_login, logout as do_logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import ModelForm, EmailInput, PasswordInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from main.models import ProfilePhoto, Profile

def profile_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in and has an associated profile, redirecting
    to the log-@user_passes_test()in page if necessary.
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
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

    def save(self, force_insert=False, force_update=False, commit=True):
        form = super(RegisterForm, self).save(commit=False)
        form.email = form.username
        if commit:
            form.save()
        return form

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
            Profile.objects.create(user=user, picture=picture,display_name="newbie")
            return redirect(reverse('login'))
        return render(request, 'sign_up.html', {'form': registerForm})

class LoginForm(Form):
    email = EmailField(max_length=255, required=True)
    password = CharField(widget=PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise ValidationError("Invalid email and password combination.")
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login()
            if user:
                do_login(request, user)
                next = request.GET['next'] if hasattr(request.GET, "next") else None
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('home'))
        else:
            return render(request, 'login.html', {'form': form})

def logout(request):
    do_logout(request)
    return redirect(reverse('home'))