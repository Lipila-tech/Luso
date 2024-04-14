from django.shortcuts import render, redirect
from django.urls import reverse
from creators.models import CreatorUser
from business.helpers import apology
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login as my_login
from django.contrib.auth.forms import AuthenticationForm
from creators.forms.forms import SignupForm, LoginForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes


def index(request):
    return render(request, 'creators/index.html')

def contribute(request, user):
    return render(request, 'creators/contribute.html')

def user_profile(request, username):
    context = {}
    try:
        # username = request.GET.get('username')
        # Logic to retrieve user data based on username (e.g., from database)
        user_data = CreatorUser.objects.get(username=username)
        context['user'] = user_data
    except CreatorUser.DoesNotExist:
        context['status'] = 404
        context['message'] = f'{username} Not Found!'
        return apology(request, context, user=username)
    return render(request, 'profile/home.html', context)


class SignupView(View):

    def get(self, request):
        form = SignupForm()
        context = {'form': form, 'category': 'Creators'}

        return render(request, 'registration/signup.html', context)

    def post(self, request):
        form = SignupForm(request.POST)
        context = {'form': form}

        try:
            if form.is_valid():
                user = form.save(commit=False)  # Don't save directly
                user.set_password(user.password)
                user.save()
                messages.add_message(request, messages.SUCCESS,
                                     "Account created successfully")
                return redirect('login')
            else:
                messages.add_message(
                    request, messages.ERROR, "Error during signup!")
                return render(request, 'registration/signup.html', context)
        except Exception as e:
            messages.add_message(
                    request, messages.ERROR, "Error during signup!")
            return render(request, 'registration/signup.html', context)
        