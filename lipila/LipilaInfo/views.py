from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as my_login
from django.contrib.auth.forms import AuthenticationForm
# My Models
from api.models import BusinessUser
from business.helpers import apology
from business.forms.forms import SignupForm, EditBusinessUserForm
from LipilaInfo.models import ContactInfo

# Public Views
def index(request):
    context = {}
    contact_info =  ContactInfo.objects.get(id=1)
    context['street'] = contact_info.street
    context['location'] = contact_info.location
    context['phone3'] = contact_info.phone1
    context['phone2'] = contact_info.phone2
    context['email1'] = contact_info.email1
    context['email2'] = contact_info.email2
    context['days'] = contact_info.days
    context['hours'] = contact_info.hours
    
    return render(request, 'UI/index.html', context)

def service_details(request):
    return render(request, 'UI/services-details.html')

def portfolio_details(request):
    return render(request, 'UI/portfolio-details.html')

def send_money(request):
    context = {}
    form = request.GET
    if form:
        payee_id = form['payee_id']
        try:
            data = BusinessUser.objects.get(username=payee_id)
            context['payee'] = payee_id
            context['location'] = data.city
        except BusinessUser.DoesNotExist:
            context = {'message': "User id not found", }
            return render(request, '404.html', context)

    return render(request, 'UI/send_money.html', context)

def pages_faq(request):
    return render(request, 'disburse/pages-faq.html')


class SignupView(View):

    def get(self, request):
        form = SignupForm()
        context = {'form': form}

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


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                my_login(request, user)
                return redirect(reverse('dashboard', kwargs={'user': username}))
        else:
            messages.error(
                request, "Your username and password didn't match. Please try again.")
            return redirect(reverse('login'))

    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# AUTHENTICATED USER VIEWS
class UpdateUserInfoView(View):
    def get(self, request, user, *args, **kwargs):
        user_object = get_object_or_404(BusinessUser, username=user)
        form = EditBusinessUserForm(instance=user_object)
        return render(request, 'disburse/profile/edit_user_info.html', {'form': form, 'user':user_object})

    def post(self, request, user, *args, **kwargs):
        user_object = get_object_or_404(BusinessUser, username=user)
        form = EditBusinessUserForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been update.")
            return redirect(reverse('profile', kwargs={'user': user_object}))
        else:
            # If form is not valid, print out the form errors for debugging
            messages.error(
                request, "Failed to update profile.")
        return render(request, 'disburse/profile/edit_user_info.html', {'form': form, 'user':user_object})