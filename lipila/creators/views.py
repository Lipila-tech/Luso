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
        

@login_required
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def dashboard(request, user):
    context = {}
    print('dashbord', user)
    #Dasboard  Reports 
    context['sales'] = 0
    context['sales_increase'] = 0
    context['revenue'] = 0
    context['increase'] = 0
    context['customers'] = 0

    # Top selling
    context['topselling'] = [
        (1245, 'product1', 199,  200, 3599),
        (1233, 'product2', 199,  200, 3599),
        (2345, 'product3', 199,  200, 3599),
        (2345, 'product4', 199,  200, 3599),
        (3333, 'product5', 199,  200, 3599),
        (4355, 'product6', 199,  200, 3599),
    ]

    # Recent sales
    context['recentsales'] = [
        ('12/03/24', 'customer1', 'product123',  343, 'Approved'),
        ('12/03/24', 'customer2', 'product123',  200, 'Approved'),
        ('12/03/24', 'customer3', 'product123',  240, 'Approved'),
        ('12/03/24', 'customer4', 'product123',  200, 'Approved'),
        ('12/03/24', 'customer5', 'product123',  200, 'Approved'),
        ('12/03/24', 'customer6', 'product123',  200, 'Approved'),
    ]


    now = datetime.now()
    request.session['last_login_time'] = now.strftime("%H:%M:%S")
    last_login_time = request.session.get('last_login_time')
    if last_login_time:
        context['last_login'] = last_login_time

    # Recent activities
    context['activities'] = [
        ('Last login', last_login_time),
        ('Receipts', 150),
        ('Pay Outs', 100),
        ('Sent Invoices', 5),
    ]

    try:
        if not user:
            raise ValueError('Username missing')
        else:
            user = CreatorUser.objects.get(username=user)
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context, user=user)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context, user=user)
    except CreatorUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user=user)
    return render(request, 'creators/admin/index.html', context)