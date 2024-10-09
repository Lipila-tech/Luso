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
from django.contrib.auth import logout as auth_logout
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


def tiktok_callback(request):
    # Get the 'code' and 'state' parameters from the URL
    code = request.GET.get('code')
    state = request.GET.get('state')
    scope = request.GET.get('scope')
    refresh_token = request.GET.get('request_token')

    # Verify that 'code' and 'state' are present
    if not code or not state:
        data = {'message': 'Server error code or state not set', 'status': 500}
        return apology(request, data)

    # Optionally: Verify the 'state' to prevent CSRF attacks
    csrf_state = request.COOKIES.get('csrfState')
    if csrf_state is None:
        data = {'message': 'Server error csrf state not set', 'status': 500}
        return apology(request, data)
    if state != csrf_state:
        data = {'message': 'Server error state not equal to csrfstate', 'status': 500}
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
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_response = py_requests.post(
        ' https://open.tiktokapis.com/v2/oauth/token/', headers=headers, data=payload)

    if token_response.status_code != 200 or "application/json" not in token_response.headers.get("content-type", ""):
        data = {'message': f'Server error {token_response}', 'status': 500}
        return apology(request, data)

    token_data = token_response.json()

    if 'access_token' in token_data:
        # Extract open_id and tokens
        open_id = token_data['open_id']
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        expires_in = token_data['expires_in']

        # Step 2: Use the access token to fetch the user's TikTok profile information
        # Add the fields as query parameters in the request URL
        user_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_info_url = 'https://open.tiktokapis.com/v2/user/info/'
        params = {
            'fields': 'open_id,union_id,avatar_url,display_name'
        }

        # Make the GET request to fetch user info
        user_info_response = py_requests.get(
            user_info_url, headers=user_headers, params=params)

        if user_info_response.status_code != 200:

            return HttpResponseBadRequest(f"Failed to retrieve user info: {user_info_response.status_code}")

        user_info = user_info_response.json()

        if 'data' not in user_info or 'user' not in user_info['data']:
            return HttpResponseBadRequest("User info not available")

        # Extract the user's TikTok username
        tiktok_username = user_info['data']['user']['display_name']
        avatar_url = user_info['data']['user']['avatar_url']

        # Check if the user already exists in UserSocialAuth
        social_auth, created = UserSocialAuth.objects.get_or_create(
            open_id=open_id,
            provider='tiktok',
            defaults={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'avatar_url': avatar_url,
                'token_expiry': timezone.now() + timedelta(seconds=expires_in),
            }
        )

        # If the UserSocialAuth was newly created, we need to create a CustomUser
        if created:
            # Create a new CustomUser
            messages.success(request, f"Congratulations {tiktok_username}! Account created.")
            user = get_user_model().objects.create(username=tiktok_username)
            # Link the social auth entry with the newly created user
            social_auth.user = user
            social_auth.save()
                
        user = authenticate(request, username=tiktok_username)
        if user is not None:
            messages.success(request, f"Login success!, {tiktok_username}!")
            login(request, user)
                # backend='accounts.auth_backends.TikTokBackend')
            request.session['tiktok_user_data'] = access_token
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, "Tiktok Authentication failed")
            return redirect(reverse('accounts:signup'))

    data = {'message': 'Tiktok Authentication failed', 'status': 500}
    return apology(request, data)


def tiktok_oauth(request):
    # Generate a random CSRF token
    csrf_state = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=16))

    # Build the TikTok authorization URL
    url = 'https://www.tiktok.com/v2/auth/authorize/'
    url += f'?client_key={TIKTOK_CLIENT_KEY}'
    url += '&scope=user.info.basic'
    url += '&response_type=code'
    url += f'&redirect_uri={TIKTOK_SERVER_ENDPOINT_REDIRECT}'
    url += f'&state={csrf_state}'

    # Set the CSRF token as a cookie
    response = redirect(url)
    response.set_cookie('csrfState', csrf_state, max_age=300, path='/')

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
        request.session['google_user_data'] = user_data
        return redirect(reverse('dashboard'))
    else:
        messages.error(request, "Authentication failed")
        return redirect(reverse('accounts:signup'))


def custom_logout(request):
    # Log out the user from Django session
    auth_logout(request)

    # Redirect URLs for third-party services
    google_logout_url = 'https://accounts.google.com/Logout'
    facebook_logout_url = 'https://www.facebook.com/logout.php'
    # Hypothetical URL, adjust if necessary
    tiktok_logout_url = 'https://www.tiktok.com/logout'

    # Check if the user logged in with a third-party service
    if 'google_user_data' in request.session:
        del request.session['google_user_data']
        return redirect('accounts:signin')
    # elif 'facebook_user_data' in request.session:
    #     # Add your Facebook access_token in the URL if needed
    #     access_token = request.session.get('facebook_access_token')
    #     return redirect(f'{facebook_logout_url}?next={settings.LOGOUT_REDIRECT_URL}&access_token={access_token}')
    elif 'tiktok_user_data' in request.session:
        del request.session['tiktok_user_data']
        return redirect('accounts:signin')

    # Default logout redirect for custom login
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
