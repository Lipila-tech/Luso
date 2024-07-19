from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

#  custom modules
from .utils import basic_auth_encode, basic_auth_decode
from .forms import SignUpForm


import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings


def sign_in(request):
    return render(request, 'registration/signin.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST.get('credential')

    if not token:
        return HttpResponse(status=400)  # Bad request if no token is provided

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID)
    except ValueError:
        return HttpResponse(status=403)  # Forbidden if token is invalid

    email = user_data.get('email')

    if not email:
        return HttpResponse(status=400)  # Bad request if no email in token

    # Get or create the user
    user, created = User.objects.get_or_create(email=email, defaults={
        'username': email.split('@')[0],  # You can modify this as needed
        'first_name': user_data.get('given_name', ''),
        'last_name': user_data.get('family_name', ''),
    })

    if created:
        messages.success(request, "Account created.")
        user.set_unusable_password()  # Set unusable password if creating a new user
        user.save()

    # Authenticate and log in the user
    user = authenticate(request, email=email)
    if user is not None:
        login(request, user)
        request.session['user_data'] = user_data
        messages.success(request, "Logged in successfully")
        return redirect(reverse('dashboard'))
    else:
        messages.error(request, "Authentication failed")
        return redirect(reverse('accounts:signup'))


def sign_out(request):
    del request.session['user_data']
    return redirect('accounts:signin')


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
        user.save()
        login(request, user)
        return redirect('patron:profile')
    else:
        return render(request, 'registration/activation_invalid.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
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


def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')  # Replace with your desired redirect URL
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
