from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
#  custom models
from .helpers import basic_auth_encode, basic_auth_decode
from .forms import SignUpForm


def activation_sent_view(request):
    return render(request, 'registration/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = basic_auth_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'registration/activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            uid64 = basic_auth_encode(user.pk)
            token = default_token_generator.make_token(user)
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid64,
                'token': token,
            })
            user.email_user(subject, message)
            return redirect('accounts:activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            user_object = User.objects.get(username=user)
            login(request, user_object)
            messages.success(request, "Logged in")
            return redirect(reverse('dashboard', kwargs={'user': username}))
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})