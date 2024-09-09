# context_processors.py
from django.conf import settings

def login_uri(request):
    return {
        'GOOGLE_LOGIN_URI': settings.GOOGLE_LOGIN_URI,
    }

def data_client_id(request):
    return {
        'CLIENT_ID': settings.GOOGLE_OAUTH_CLIENT_ID,
    }