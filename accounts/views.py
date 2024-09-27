import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

#  custom modules
from lipila.utils import apology
from .utils import basic_auth_encode, basic_auth_decode
from .forms import SignUpForm
from accounts.models import UserSocialAuth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
import requests as py_requests
import random
import string

TIKTOK_CLIENT_KEY = settings.TIKTOK_CLIENT_KEY
TIKTOK_SERVER_ENDPOINT_REDIRECT = settings.TIKTOK_SERVER_ENDPOINT_REDIRECT
TIKTOK_CLIENT_SECRET = settings.TIKTOK_CLIENT_SECRET
MTN_TOKEN_URL = settings.MTN_TOKEN_URL


def momo_callback(request):
    # Get the 'code' parameter from the URL
    authorization_code = request.GET.get('code')
    state = request.GET.get('state')  # If using state for CSRF protection

    # Validate the presence of 'code'
    if not authorization_code:
        return HttpResponseBadRequest("Missing authorization code")

    # Optionally: Verify the state to prevent CSRF attacks
    csrf_state = request.COOKIES.get('csrfState')
    if state != csrf_state:
        return HttpResponseBadRequest("Invalid state parameter")

    # Exchange the authorization code for an access token
    token_url = MTN_TOKEN_URL
    headers = {
        'Authorization': 'Basic YOUR_BASE64_ENCODED_CLIENT_ID_AND_SECRET',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'YOUR_REDIRECT_URI'
    }

    # Make the POST request to get the access token
    token_response = requests.post(token_url, headers=headers, data=payload)

    # Check if the request was successful
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        # Handle the access token (store it, use it, etc.)
        return HttpResponse(f"Access token obtained: {access_token}")
    else:
        return HttpResponseBadRequest(f"Failed to get access token: {token_response.text}")


def tiktok_callback(request):
    # Get the 'code' and 'state' parameters from the URL
    code = request.GET.get('code')
    state = request.GET.get('state')
    scope = request.GET.get('scope')
    refresh_token = request.GET.get('request_token')

    # Verify that 'code' and 'state' are present
    if not code or not state:
        data = {'message': 'Server error', 'status': 500}
        return apology(request, data)

    # Optionally: Verify the 'state' to prevent CSRF attacks
    csrf_state = request.COOKIES.get('csrfState')
    if csrf_state is None:
        data = {'message': 'Server error', 'status': 500}
        return apology(request, data)
    if state != csrf_state:
        data = {'message': 'Server error', 'status': 500}
        return apology(request, data)

    # Now you can use the 'code' to exchange for an access token
    # Example: make a POST request to TikTok's token endpoint
    payload = {
        'client_key': TIKTOK_CLIENT_KEY,
        'client_secret': TIKTOK_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': TIKTOK_SERVER_ENDPOINT_REDIRECT
    }
    token_response = py_requests.post(
        'https://www.tiktok.com/v2/tiktok_oauth/token/', data=payload)
    
    if token_response.status_code != 200 or "application/json" not in token_response.headers.get("content-type", ""):
        data = {'message': 'Server error', 'status': 500}
        return apology(request, data)

    token_data = token_response.json()

    if 'access_token' in token_data:
        # Extract open_id and tokens
        open_id = token_data['open_id']
        username = token_data['username']
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        expires_in = token_data['expires_in']

        # Check if the user already exists in UserSocialAuth
        social_auth, created = UserSocialAuth.objects.get_or_create(
            open_id=open_id,
            provider='tiktok',
            defaults={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_expiry': timezone.now() + timedelta(seconds=expires_in),
            }
        )

        # If the UserSocialAuth was newly created, we need to create a CustomUser
        if created:
            # Create a new CustomUser
            user = get_user_model().objects.create(username=username)
            # Link the social auth entry with the newly created user
            social_auth.user = user
            social_auth.save()
        else:
            # User already exists, retrieve the user
            user = social_auth.user
            # Authenticate and log in the user
            messages.success(request, f"Welcome back, {user.username}!")

        # Log the user in
        login(request, user, backend='accounts.auth_backends.EmailOrUsernameModelBackend')

        return redirect(reverse('dashboard'))
    else:
        messages.error(request, "Authentication failed")
        return redirect(reverse('accounts:signup'))


def tiktok_oauth(request):
    # Generate a random CSRF token
    csrf_state = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=16))

    # Build the TikTok authorization URL
    url = 'https://www.tiktok.com/v2/auth/authorize/'
    url += f'?client_key={TIKTOK_CLIENT_KEY}'
    url += '&scope=user.info.basic, video.list, user.info.profile'
    url += '&response_type=code'
    url += f'&redirect_uri={TIKTOK_SERVER_ENDPOINT_REDIRECT}'
    url += f'&state={csrf_state}'

    # Set the CSRF token as a cookie
    response = redirect(url)
    response.set_cookie('csrfState', csrf_state, max_age=60)

    # Redirect to the TikTok authorization URL
    return response


def sign_in(request):
    return render(request, 'registration/signin.html')


@csrf_exempt
def google_callback(request):
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
    user, created = get_user_model().objects.get_or_create(email=email, defaults={
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
        messages.success(request, f"Welcome back, {user.username}!")
        login(request, user)
        request.session['user_data'] = user_data
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
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated please login")
        return redirect('accounts:signin')
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
            messages.error(request, "Invalid form fields.")
            form = SignUpForm()
            return render(request, 'registration/signup.html', {'form': form})

    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        next_url = request.GET.get('next', 'dashboard')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.has_group or user.is_staff:
                    messages.success(
                        request, f"Welcome back, {user.username}!")
                    return redirect(next_url)
                else:
                    return redirect('patron:create_creator_profile')
            else:
                form = AuthenticationForm()
                return render(request, 'registration/login.html', {'form': form})
        else:
            messages.error(request, "Invalid username or password.")
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
