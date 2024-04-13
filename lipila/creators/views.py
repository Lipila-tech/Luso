from django.shortcuts import render
from business.models import BusinessUser
from business.helpers import apology

def index(request):
    return render(request, 'creators/index.html')

def contribute(request, user):
    return render(request, 'creators/contribute.html')

def user_profile(request, username):
    context = {}
    try:
        # username = request.GET.get('username')
        # Logic to retrieve user data based on username (e.g., from database)
        user_data = BusinessUser.objects.get(username=username)
        context['user'] = user_data
    except BusinessUser.DoesNotExist:
        context['status'] = 404
        context['message'] = f'{username} Not Found!'
        return apology(request, context, user=username)
    return render(request, 'profile/home.html', context)